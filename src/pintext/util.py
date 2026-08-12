import pint

from .exceptions import UnitsError


def units_compatible(unit1: pint.Unit, unit2: pint.Unit) -> bool:
    """
    Check if two units are compatible. Accounts for angle units.

    :param unit1:
        First unit to check for compatibility.

    :param unit2:
        Second unit to check for compatibility.

    :returns:
        ``True`` if ``unit1`` and ``unit2`` have the same dimensionality,
        ``False`` otherwise.

    .. rubric:: Examples

    >>> units_compatible(ureg.m, ureg.km)
    True
    >>> units_compatible(ureg.m, ureg.s)
    False

    Angles are deliberately *not* considered compatible with dimensionless
    values, even though Pint converts between them:

    >>> units_compatible(ureg.rad, ureg.dimensionless)
    False
    >>> units_compatible(ureg.sr, ureg.rad)
    False
    """
    return (1.0 * unit1 / unit2).unitless


def check_units(value, units: pint.Unit, name: str | None = None) -> None:
    """
    Check that a value carries units compatible (in the sense of
    :func:`.units_compatible`) with ``units``.

    This is the framework-agnostic unit check shared by the *attrs* and
    *pydantic* integrations.

    :param value:
        Value to check. Expected to be a :class:`pint.Quantity`.

    :param units:
        Units ``value`` must be compatible with.

    :param name:
        Name of the field being checked, used to build the error message. If
        ``None``, a generic message is produced.

    :raises UnitsError:
        If units are incompatible, or if a unitless value is provided.

    .. rubric:: Examples

    >>> check_units(1.0 * ureg.km, ureg.m)

    An incompatible value raises:

    >>> check_units(1.0 * ureg.s, ureg.m)
    Traceback (most recent call last):
      ...
    pintext.exceptions.UnitsError: Cannot convert from 'second' to 'meter': ...
    """
    target = f"field '{name}'" if name is not None else "value"

    try:
        value_units = value.units
    except AttributeError as e:  # value.units doesn't exist
        raise UnitsError(
            units1=None,
            units2=units,
            extra_msg=f": unitless value '{value}' "
            f"used to set {target} "
            f"(requires units '{units}').",
        ) from e

    if not units_compatible(value_units, units):
        raise UnitsError(
            units1=value_units,
            units2=units,
            extra_msg=f": incompatible units '{value_units}' "
            f"used to set {target} "
            f"(allowed: '{units}').",
        )
