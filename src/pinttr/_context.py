from contextlib import ExitStack, contextmanager
from typing import Callable, Dict, Hashable, Optional, Union

import attrs
import pint

from ._defaults import get_unit_registry
from ._func import identity
from ._generator import UnitGenerator


@attrs.define
class UnitContext:
    """
    An overridable registry of :class:`.UnitGenerator` objects.

    This class maintains a registry of :class:`.UnitGenerator` instances.
    Stored :class:`.UnitGenerator` objects can be conveniently overridden using
    the :meth:`.override` context manager.

    :Attributes / constructor arguments:

        * **registry** (Dict[Hashable, :class:`~pinttrs.UnitGenerator`]) –
          Unit generator registry. Keys can be any hashable type, but
          :class:`str` or :class:`~enum.Enum` are recommended.
          Defaults to an empty dictionary.

          .. note:: The initialisation sequence will make repeated calls to
             :meth:`register` and will consequently apply the same key and value
             conversion rules.

        * **interpret_str** (:class:`bool`) –
          If ``True``, attempt string-to-units interpretation when specifying
          unit generators as :class:`str`.

        * **ureg** (Optional[:class:`~pint.UnitRegistry`]) –
          Unit registry used for string-to-units interpretation. If ``None``,
          the default registry is used (see :func:`.get_unit_registry`).

        * **key_converter** (Callable) –
          Converter used for keys. Defaults to :func:`.identity`.

    .. versionchanged:: 1.1.0
       Added ``ureg``.
    """

    registry: Dict[Hashable, UnitGenerator] = attrs.field(factory=dict)
    interpret_str: bool = attrs.field(default=False)
    ureg: Optional[pint.UnitRegistry] = attrs.field(default=None)
    key_converter: Callable = attrs.field(default=identity)

    def __attrs_post_init__(self):
        # Convert keys when relevant
        for key in list(self.registry.keys()):
            self._convert_key(key)
        # Convert values when relevant
        for key in self.registry.keys():
            self._convert_value(key)

    def _convert_key(self, key):
        """
        Apply in-place conversion rule ``key_converter`` to a registered key.

        :param key:
            Key to which conversion is to be applied.
        """
        self.registry[self.key_converter(key)] = self.registry.pop(key)

    def _convert_value(self, key):
        """
        Apply conversion rules to a registered value. Registry values specified
        as :class:`pint.Unit` will be converted to :class:`UnitGenerator`
        instances. If string-to-units interpretation is activated, units will be
        converted to :class:`pint.Unit` objects using ``self.ureg`` if it is
        set, or the default registry returned by :func:`.get_unit_registry`
        otherwise.

        :param key:
            Key to the value to which conversion is to be applied.
        """
        key = self.key_converter(key)
        value = self.registry[key]

        # Interpret units specified as string if necessary
        if isinstance(value, str):
            if self.interpret_str:
                value = (
                    self.ureg.Unit(value)
                    if self.ureg is not None
                    else get_unit_registry().Unit(value)
                )
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

    def register(
        self, key: Hashable, value: Union[UnitGenerator, pint.Unit, str]
    ) -> None:
        """
        Add or update an entry in the registry. Conversion rules are applied as
        follows:

        * ``key`` is applied the ``key_converter`` converter;
        * ``value`` is converted to a :class:`UnitGenerator`.

        In addition, if ``interpret_str`` is ``True``, ``value`` can be
        specified as a string. In that case, it will be converted to a
        :class:`pint.Unit` using the unit registry returned by
        :func:`.get_unit_registry`.

        :param key:
            Key to the registered entry.

        :param value:
            Object to register.
        """
        self.registry[key] = value
        self._convert_key(key)
        self._convert_value(key)

    def update(self, d: Dict) -> None:
        """
        Update the registry with a dictionary.

        :param d:
            Dictionary used to apply :meth:`register` for each of its key-value
            pairs.
        """
        for key, value in d.items():
            self.register(key, value)

    def get(self, key: Hashable) -> pint.Unit:
        """
        Evaluate :class:`UnitGenerator` instance registered as ``key``.

        :param key:
            Key to the :class:`UnitGenerator` to evaluate. The ``key_converter``
            is applied.

        :returns:
            Evaluated units.
        """
        key = self.key_converter(key)

        try:
            return self.registry[key]()
        except KeyError:
            raise

    def get_all(self) -> Dict[Hashable, pint.Unit]:
        """
        Evaluate all registered :class:`UnitGenerator` instance.

        :returns:
            Evaluated units as a dictionary.
        """
        return {key: self.get(key) for key in self.registry.keys()}

    def deferred(self, key: Hashable) -> UnitGenerator:
        """
        Return the :class:`UnitGenerator` registered with a given key.

        :param key:
            Key to the :class:`UnitGenerator` to return. The ``key_converter``
            is applied.

        :returns:
            Unit generator.
        """
        key = self.key_converter(key)
        return self.registry[key]

    @contextmanager
    def override(self, *args, **kwargs) -> None:
        """
        Temporarily override underlying unit generators. This method acts as a
        convenience proxy for :meth:`UnitGenerator.override`.

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

    def __getitem__(self, key: Hashable) -> pint.Unit:
        """
        Alias to :meth:`.get`.

        :param key:
            Key to the :class:`UnitGenerator` to evaluate. The ``key_converter``
            is applied.

        :returns:
            Evaluated units.

        .. versionadded:: 21.2.0
        """
        return self.get(key)

    def __setitem__(
        self, key: Hashable, value: Union[UnitGenerator, pint.Unit, str]
    ) -> None:
        """
        Alias to :meth:`register`.

        :param key:
            Key to the registered entry.

        :param value:
            Object to register.

        .. versionadded:: 21.2.0
        """
        self.register(key, value)
