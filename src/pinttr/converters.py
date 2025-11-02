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

    The following types are supported:

    * :class:`dict` (or, more generally, mappings): the magnitude (resp. units)
      must be supplied as the ``value``, ``magnitude`` or ``m`` keys (resp.
      ``units`` or ``u``).
    * :class:`xarray.DataArray`: the magnitude is the underlying data array
      (converted to a NumPy array) and units are read from the ``units``
      attribute. If the ``units`` attribute is missing, the DataArray is
      returned unchanged.

    :param value: Object to attempt conversion on.
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
