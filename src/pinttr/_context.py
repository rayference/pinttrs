from contextlib import ExitStack, contextmanager
from copy import copy

import attr
import pint

from ._defaults import get_unit_registry
from .converters import identity


@attr.s
class UnitGenerator:
    """
    A callable object which returns units objects.
    Stored units can be contextually overridden using the :meth:`.override`
    method.

    .. seealso:: :class:`.UnitContext`

    :Attributes / constructor arguments:

        **units** (:class:`pint.Unit` or callable) – Stored units or generator.
    """

    units = attr.ib()

    def __call__(self):
        """
        :returns: If ``units`` is a :class:`pint.Unit`, it is returned;
            if ``units`` is a callable, the result of its evaluation will be
            returned.

        :rtype: :class:`pint.Unit`
        """
        if callable(self.units):
            return self.units()
        return self.units

    @contextmanager
    def override(self, units):
        """
        Temporarily override the value of ``units``. The initial value of
        ``units`` is restored upon leaving context.

        :param units: Temporary replacement for ``units``.

        :type units: :class:`pint.Unit` or callable
        """
        units_old = copy(self.units)

        if isinstance(units, str):  # Safeguard to convert strings
            if callable(self.units):
                self.units = self.units()._REGISTRY.Unit(units)
            else:
                self.units = self.units._REGISTRY.Unit(units)
        else:
            self.units = units
        try:
            yield
        finally:
            self.units = units_old


@attr.s
class UnitContext:
    """
    An overridable registry of :class:`.UnitGenerator` objects.

    This class maintains a registry of :class:`.UnitGenerator` instances.
    Stored :class:`.UnitGenerator` objects can be conveniently overridden using
    the :meth:`.override` context manager.

    :Attributes / constructor arguments:

        * **registry** (dict[Hashable, :class:`.UnitGenerator`]) – Unit
          generator registry. Keys can be any hashable type, but :class:`str`
          or :class:`~enum.Enum` are recommended.

          .. note:: The initialisation sequence will make repeated calls to
             :meth:`register` and will consequently apply the same key and value
             conversion rules.

        * **interpret_str** (:class:`bool`) – If ``True``, attempt
          string-to-units interpretation when specifying unit generators as
          :class:`str`.

        * **key_converter** (callable) – Converter used for keys. Defaults to
          :func:`.identity`.
    """

    registry = attr.ib(default={})
    interpret_str = attr.ib(default=False)
    key_converter = attr.ib(default=identity)

    def __attrs_post_init__(self):
        # Convert keys when relevant
        for key in list(self.registry.keys()):
            self._convert_key(key)
        # Convert values when relevant
        for key in self.registry.keys():
            self._convert_value(key)

    def _convert_key(self, key):
        """
        Apply conversion rule ``key_converter`` to a registered key.

        :param key: Key to which conversion is to be applied.
        """
        self.registry[self.key_converter(key)] = self.registry.pop(key)

    def _convert_value(self, key):
        """
        Apply conversion rules to a registered value. Registry values specified
        as :class:`pint.Unit` will be converted to :class:`UnitGenerator`
        instances. If string-to-units interpretation is activated, units will be
        converted to :class:`pint.Unit` objects using the default registry
        returned by :func:`.get_unit_registry`.

        :param key: Key to the value to which conversion is to be applied.
        """
        key = self.key_converter(key)
        value = self.registry[key]

        # Interpret units specified as string if necessary
        if isinstance(value, str):
            if self.interpret_str:
                value = get_unit_registry().Unit(value)
            else:
                raise TypeError("String-to-units interpretation is disabled")

        # Proceed with actual registration
        if isinstance(value, pint.Unit):
            self.registry[key] = UnitGenerator(value)
        elif isinstance(value, UnitGenerator):
            self.registry[key] = value
        else:
            raise TypeError(
                f"Items must be either str, pint.Unit or UnitGenerator; "
                f"found: {key}: {type(value)}"
            )

    def register(self, key, value):
        """
        Add or update an entry in the registry. Conversion rules are applied as
        follows:

        * ``key`` is applied the ``key_converter`` converter;
        * ``value`` is converted to a :class:`UnitGenerator`.

        In addition, if ``interpret_str`` is ``True``, ``value`` can be
        specified as a string. In that case, it will be converted to a
        :class:`pint.Unit` using the unit registry returned by
        :func:`.get_unit_registry`.

        :param key: Key to the registered entry.

        :type key: Hashable

        :param value: Object to register.

        :type value: :class:`UnitGenerator` or :class:`pint.Unit` or
            :class:`str`
        """
        self.registry[key] = value
        self._convert_key(key)
        self._convert_value(key)

    def update(self, d):
        """
        Update the registry with a dictionary.

        :param d: Dictionary used to apply :meth:`register` for each of its
            key-value pairs.

        :type d: :class:`dict`
        """
        for key, value in d.items():
            self.register(key, value)

    def get(self, key):
        """
        Evaluate :class:`UnitGenerator` instance registered as ``key``.

        :param key: Key to the :class:`UnitGenerator` to evaluate. The 
            ``key_converter`` is applied.

        :type key: Hashable

        :returns: Evaluated units.

        :rtype: :class:`pint.Unit`
        """
        key = self.key_converter(key)

        try:
            return self.registry[key]()
        except KeyError:
            raise

    def get_all(self):
        """
        Evaluate all registered :class:`UnitGenerator` instance.

        :returns: Evaluated units as a dictionary.

        :rtype: dict[Hashable, :class:`pint.Unit`]
        """
        return {key: self.get(key) for key in self.registry.keys()}

    def deferred(self, key):
        """
        Return the :class:`UnitGenerator` registered with a given key.

        :param key: Key to the :class:`UnitGenerator` to return. The
            ``key_converter`` is applied.

        :type key: Hashable

        :returns: Unit generator.

        :rtype: :class:`UnitGenerator`
        """
        key = self.key_converter(key)
        return self.registry[key]

    @contextmanager
    def override(self, *args, **kwargs):
        """
        Temporarily override the underlying unit generators. This method
        acts as a convenience proxy for :meth:`UnitGenerator.override`.

        Override specifications can take multiple forms:

        * an arbitrary number of dictionaries can be passed as positional 
          arguments;
        * key-value pairs may also be specified as keyword arguments.

        Both approaches can be mixed. 
        
        .. note:: When using the keyword argument specification, passed values 
           will systematically be strings. Consequently, either

           * registry keys must be strings;
           * or the ``key_converter`` must provide the conversion protocol for
             string-valued keys.
        """
        with ExitStack() as stack:
            for arg in args:
                if not isinstance(arg, dict):
                    raise TypeError
                for key, value in arg.items():
                    stack.enter_context(
                        self.registry[self.key_converter(key)].override(value)
                    )

            for key, value in kwargs.items():
                stack.enter_context(
                    self.registry[self.key_converter(key)].override(value)
                )

            try:
                yield
            finally:
                pass
