from typing import Any, Callable, Union

import pint


def always_iterable(obj, base_type=(str, bytes)):
    """
    Ensure that the object it is passed is iterable.

    - If ``obj`` is iterable, return an iterator over its items.
    - If ``obj`` is not iterable, return a one-item iterable containing ``obj``.
    - If ``obj`` is ``None``, return an empty iterable.

    By default, binary and text strings are not considered iterable.
    If ``base_type`` is set, objects for which ``isinstance(obj, base_type)``
    returns ``True`` won't be considered iterable.

    Set ``base_type`` to ``None`` to avoid any special handling and treat
    objects Python considers iterable as iterable.

    .. note::

        Copied from :func:`more_itertools.always_iterable`.
    """
    if obj is None:
        return iter(())

    if (base_type is not None) and isinstance(obj, base_type):
        return iter((obj,))

    try:
        return iter(obj)
    except TypeError:
        return iter((obj,))


def ensure_units(
    value: Any,
    default_units: Union[pint.Unit, Callable],
    convert: bool = False,
) -> pint.Quantity:
    """Ensure that a value is wrapped in a Pint quantity container.

    :param value:
        Value to ensure the wrapping of.

    :param default_units:
        Units to use to initialise the :class:`pint.Quantity` if ``value`` is
        not a :class:`pint.Quantity`. A callable can be passed;
        in this case, the applied units will be ``default_units()``.

    :param convert:
        If ``True``, ``value`` will also be converted to ``default_units`` if it
        is a :class:`pint.Quantity`.

    :returns:
        Converted ``value``.
    """
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
    """
    return (1.0 * unit1 / unit2).unitless
