from collections.abc import Mapping
from functools import partial
from typing import Any, Callable, Union

import attrs
import pint

from ._defaults import get_unit_registry
from ._generator import UnitGenerator


def to_units(units: Union[pint.Unit, UnitGenerator]) -> Callable[[Any], pint.Quantity]:
    """
    Create a callable ``f(x)`` returning
    :func:`ensure_units(x, units, convert=False) <pinttrs.converters.ensure_units>`.

    :param units:
        Units to ensure conversion to.

    .. deprecated:: 25.2.0
       Prefer :func:`pinttrs.converters.ensure_units` in its
       deferred form.
    """
    return ensure_units(default_units=units)


def ensure_units(
    maybe_value: Any = attrs.NOTHING,
    *,
    default_units: Union[pint.Unit, Callable],
    convert: bool = False,
) -> Any:
    """
    Ensure that a value is wrapped in a Pint quantity container.

    This converter can be used in two modes:

    1. **Immediate mode**: Pass a value to convert it directly.
    2. **Deferred mode**: Omit the value to get a converter function.

    :param maybe_value:
        Value to ensure the wrapping of. If not supplied, this function returns
        a converter with the signature ``f(x: Any) -> Any`` that is effectively
        ``functools.partial(ensure_units, default_units=default_units, convert=convert)``.

    :param default_units:
        Units to use to initialize the :class:`pint.Quantity` if ``maybe_value``
        is not a :class:`pint.Quantity`. A callable can be passed;
        in this case, the applied units will be ``default_units()``.

    :param convert:
        If ``True``, ``maybe_value`` will also be converted to ``default_units``
        if it is a :class:`pint.Quantity`.

    :returns:
        Converted ``maybe_value`` if specified; otherwise, a converter function.

    .. rubric:: Examples

    * **Immediate mode**. Convert a value directly:

      >>> ensure_units(100.0, default_units=ureg.m)
      <Quantity(100.0, 'meter')>

      By default, quantities with units are passed through unchanged:

      >>> ensure_units(100.0 * ureg.km, default_units=ureg.m)
      <Quantity(100.0, 'kilometer')>

      Set ``convert=True`` to force conversion to the default units:

      >>> ensure_units(100.0 * ureg.km, default_units=ureg.m, convert=True)
      <Quantity(100000.0, 'meter')>

    * **Deferred mode**: Create a converter function:

      >>> converter = ensure_units(default_units=ureg.km)
      >>> converter(5.0)
      <Quantity(5.0, 'kilometer')>
      >>> converter(100.0 * ureg.m)
      <Quantity(100.0, 'meter')>

      This is particularly useful with attrs:

      >>> @attrs.define
      ... class Circle:
      ...     radius = attrs.field(converter=ensure_units  (default_units=ureg.m))
      >>> Circle(radius=100.0)
      Circle(radius=<Quantity(100.0, 'meter')>)
      >>> Circle(radius=5.0 * ureg.km)
      Circle(radius=<Quantity(5.0, 'kilometer')>)

    .. versionchanged:: 21.1.0
       Relocated from ``pinttr.converters`` to ``pinttr.util``.

    .. versionchanged:: 25.2.0
       Relocated again from ``pinttr.util`` to ``pinttr.converters``. The
       previous is kept as an alias and is deprecated.

    .. versionchanged:: 25.2.0
       The first argument is now optional, which allows both deferred and
       immediate executions.
    """

    if maybe_value is attrs.NOTHING:
        if not isinstance(default_units, (pint.Unit, UnitGenerator)):
            raise TypeError("Argument 'units' must be a pint.Units or a UnitGenerator")

        return partial(ensure_units, default_units=default_units, convert=convert)

    value = maybe_value

    if callable(default_units):
        units = default_units()
    else:
        units = default_units

    if not isinstance(units, pint.Unit):
        raise TypeError("Argument 'units' must be a pint.Units or a UnitGenerator")

    if isinstance(value, pint.Quantity):
        if convert:
            return value.to(units)
        else:
            return value
    else:
        return value * units


def to_quantity(value: Any) -> Any:
    """
    Attempts turning an object into a Pint quantity. Unsupported types are
    simply passed through.

    This converter is useful for loading data from serialized formats (JSON, YAML)
    or working with xarray DataArrays that follow CF conventions.

    The following types are supported:

    * :class:`dict` (or, more generally, mappings): the magnitude (resp. units)
      must be supplied as the ``value``, ``magnitude`` or ``m`` keys (resp.
      ``units`` or ``u``).
    * :class:`xarray.DataArray`: the magnitude is the underlying data array
      (converted to a NumPy array) and units are read from the ``units``
      attribute. If the ``units`` attribute is missing, the DataArray is
      returned unchanged. If the xarray dependency is not installed, conversion
      is skipped.

    .. warning::
       * This converter uses the global unit registry from
         :func:`~pinttrs.get_unit_registry`.
       * Extra keys in dictionaries will raise a ``ValueError``.

    :param value:
        Object to attempt conversion on.

    :raises ValueError:
        When converting a dictionary, if a magnitude or unit key is missing.

    :raises ValueError:
        When converting a dictionary, if unhandled keys are supplied.

    .. rubric:: Examples

    * **Converting dictionaries**: Useful for loading from JSON or YAML files:

      >>> to_quantity({"value": 1.0, "units": "m"})
      <Quantity(1.0, 'meter')>
      >>> to_quantity({"magnitude": 2.5, "units": "km"})
      <Quantity(2.5, 'kilometer')>

      Shorter key names are also supported:

      >>> to_quantity({"m": 100.0, "u": "cm"})
      <Quantity(100.0, 'centimeter')>

      Unsupported types pass through unchanged:

      >>> to_quantity(42.0)
      42.0
      >>> to_quantity("text")
      'text'

    * **Converting xarray DataArrays**: Extracts data and units from DataArrays
      following CF conventions (requires xarray):

      >>> data = xr.DataArray([1.0, 2.0, 3.0], attrs={"units": "m"})
      >>> to_quantity(data)
      <Quantity([1. 2. 3.], 'meter')>

      DataArrays without units are passed through:

      >>> data = xr.DataArray([1.0, 2.0])
      >>> to_quantity(data)  # doctest: +ELLIPSIS
      <xarray.DataArray (dim_0: 2)>...
    """

    ureg = get_unit_registry()

    # Handle xarray DataArray
    try:
        import xarray as xr

        if isinstance(value, xr.DataArray):
            if hasattr(value, "attrs") and "units" in value.attrs:
                magnitude = value.values
                units = value.attrs["units"]
                value = ureg.Quantity(magnitude, units)
            return value
    except ImportError:
        pass

    # Handle mappings (dict-like objects)
    if isinstance(value, Mapping):
        value = dict(value)
        for k_m in ["value", "magnitude", "m"]:
            try:
                magnitude = value.pop(k_m)
            except KeyError:
                continue
            break
        else:
            raise ValueError("Supplied value has no magnitude")

        for k_u in ["units", "u"]:
            try:
                units = value.pop(k_u)
            except KeyError:
                continue
            break
        else:
            raise ValueError("Supplied value has no units")

        if len(value) > 0:
            raise ValueError(
                f"Supplied value has extra unused keys {list(value.keys())}"
            )

        value = ureg.Quantity(magnitude, units)

    return value
