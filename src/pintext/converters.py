from collections.abc import Callable, Mapping
from functools import partial
from tokenize import TokenError
from typing import Any

import pint
from pint import UndefinedUnitError

from ._generator import UnitGenerator
from ._registry import get_unit_registry
from ._sentinel import NOTHING

# Exceptions raised by Pint when it fails to interpret a string
_PINT_PARSE_ERRORS = (UndefinedUnitError, TokenError, AssertionError, ArithmeticError)


def ensure_units(
    maybe_value: Any = NOTHING,
    *,
    default_units: pint.Unit | Callable[[], pint.Unit],
    convert: bool = False,
) -> Any:
    """
    Ensure that a value is wrapped in a Pint quantity container.

    This converter can be used in two modes:

    * **Immediate mode**: Pass a value to convert it directly.
    * **Deferred mode**: Omit the value to get a converter function.

    :param maybe_value:
        Value to ensure the wrapping of. If not supplied, this function returns
        a converter with the signature ``f(x: Any) -> Any`` that is effectively
        ``functools.partial(ensure_units, default_units=default_units,
        convert=convert)``.

    :param default_units:
        Units to use to initialize the :class:`pint.Quantity` if ``maybe_value``
        is not a :class:`pint.Quantity`. A callable can be passed;
        in this case, the applied units will be ``default_units()``.

    :param convert:
        If ``True``, ``maybe_value`` will also be converted to ``default_units``
        if it is a :class:`pint.Quantity`.

    :returns:
        Converted ``maybe_value`` if specified; otherwise, a converter function.

    :raises pint.UndefinedUnitError:
        If ``maybe_value`` is a string Pint cannot parse.

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

      Strings are parsed by the default registry; those that carry no units are
      treated as unitless values:

      >>> ensure_units("2 m", default_units=ureg.km)
      <Quantity(2, 'meter')>
      >>> ensure_units("2", default_units=ureg.km)
      <Quantity(2, 'kilometer')>

    * **Deferred mode**: Create a converter function:

      >>> converter = ensure_units(default_units=ureg.km)
      >>> converter(5.0)
      <Quantity(5.0, 'kilometer')>
      >>> converter(100.0 * ureg.m)
      <Quantity(100.0, 'meter')>

      Deferred units are reevaluated on every call, which allows leveraging unit
      context overrides dynamically:

      >>> generator = UnitGenerator(ureg.m)
      >>> converter = ensure_units(default_units=generator)
      >>> converter(1.0)
      <Quantity(1.0, 'meter')>
      >>> with generator.override(ureg.km):
      ...     converter(1.0)
      <Quantity(1.0, 'kilometer')>
    """

    if maybe_value is NOTHING:
        if not isinstance(default_units, (pint.Unit, UnitGenerator)):
            raise TypeError(
                "Argument 'default_units' must be a pint.Unit or a UnitGenerator"
            )

        return partial(ensure_units, default_units=default_units, convert=convert)

    value = maybe_value

    if isinstance(default_units, pint.Unit):
        units = default_units
    else:
        units = default_units()

    if not isinstance(units, pint.Unit):
        raise TypeError(
            "Argument 'default_units' must be a pint.Unit or a UnitGenerator"
        )

    if isinstance(value, str):
        # Strings must be parsed by the registry: multiplying a string by units
        # produces a quantity whose magnitude is the string itself
        ureg = get_unit_registry()
        parsed = ureg.Quantity(value)
        # A bare number parses as dimensionless: keep it unitless so that the
        # default units are applied to it
        value = parsed.magnitude if parsed.units == ureg.dimensionless else parsed

    if isinstance(value, pint.Quantity):
        if convert:
            return value.to(units)
        else:
            return value
    else:
        return value * units


def to_quantity(value: Any, strict: bool = False) -> Any:
    """
    Attempts turning an object into a Pint quantity.

    Values for which conversion fails are passed through, unless ``strict`` mode
    is active.

    This converter is useful for loading data from serialized formats (JSON,
    YAML) or working with xarray DataArrays that carry units in a
    Pint-compatible format.

    The following types are supported:

    * :class:`pint.Quantity`: passed through unchanged.
    * :class:`dict` (or, more generally, mappings): the magnitude (resp. units)
      must be supplied as the ``value``, ``magnitude`` or ``m`` keys (resp.
      ``units``, ``unit`` or ``u``).
    * :class:`xarray.DataArray`: the magnitude is the underlying data array
      (converted to a NumPy array) and units are read from the ``units``
      attribute. If the ``units`` attribute is missing, the DataArray is
      returned unchanged. If the xarray dependency is not installed, conversion
      is skipped.
    * Other types are tentatively converted by Pint. This, in particular,
      parses unit-carrying strings and applies dimensionless units to unitless
      values.

    .. warning::
        * This converter uses the global unit registry from
          func:`~pintext.get_unit_registry`.
        * Extra keys in dictionaries will raise a ``ValueError``.

    :param value:
        Object to attempt conversion on.

    :param strict:
        If ``True``, failed conversion raises a ``ValueError``.

    :raises ValueError:
        When converting a dictionary, if a magnitude or unit key is missing.

    :raises ValueError:
        When converting a dictionary, if unhandled keys are supplied.

    :raises ValueError:
        When conversion to a quantity fails and ``strict`` is ``True``.

    .. rubric:: Examples

    * **Converting dictionaries**: Useful for loading from JSON or YAML files:

      >>> to_quantity({"value": 1.0, "units": "m"})
      <Quantity(1.0, 'meter')>
      >>> to_quantity({"magnitude": 2.5, "units": "km"})
      <Quantity(2.5, 'kilometer')>

      Shorter key names are also supported:

      >>> to_quantity({"m": 100.0, "u": "cm"})
      <Quantity(100.0, 'centimeter')>

    * **Converting xarray DataArrays**: Extracts data and units from DataArrays
      following CF conventions (requires xarray):

      >>> data = xr.DataArray([1.0, 2.0, 3.0], attrs={"units": "m"})
      >>> to_quantity(data)
      <Quantity([1. 2. 3.], 'meter')>

      DataArrays without units are passed through:

      >>> data = xr.DataArray([1.0, 2.0])
      >>> to_quantity(data)  # doctest: +ELLIPSIS
      <xarray.DataArray (dim_0: 2)>...

    * **Converting other types**: unit-carrying strings are parsed, unitless
      values become dimensionless quantities:

      >>> to_quantity("2 m")
      <Quantity(2, 'meter')>
      >>> to_quantity(42.0)
      <Quantity(42.0, 'dimensionless')>

      Values Pint cannot interpret pass through, unless ``strict`` is ``True``:

      >>> to_quantity("text")
      'text'
      >>> to_quantity("text", strict=True)
      Traceback (most recent call last):
          ...
      ValueError: Conversion of value to quantity failed (got 'text')
    """

    ureg = get_unit_registry()

    # Quantities are passed through
    if isinstance(value, pint.Quantity):
        return value

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
        value_ = dict(value)
        for k_m in ["value", "magnitude", "m"]:
            try:
                magnitude = value_.pop(k_m)
            except KeyError:
                continue
            break
        else:
            raise ValueError("Supplied value has no magnitude")

        for k_u in ["units", "unit", "u"]:
            try:
                units = value_.pop(k_u)
            except KeyError:
                continue
            break
        else:
            raise ValueError("Supplied value has no units")

        if len(value_) > 0:
            raise ValueError(
                f"Supplied value has extra unused keys {list(value_.keys())}"
            )

        return ureg.Quantity(magnitude, units)

    # Handle other types
    try:
        return ureg.Quantity(value)
    except (*_PINT_PARSE_ERRORS, TypeError):
        pass

    if strict:
        raise ValueError(f"Conversion of value to quantity failed (got {value!r})")

    return value
