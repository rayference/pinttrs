from typing import Any, Callable, Union

import pint


def ensure_units(
    value: Any,
    default_units: Union[pint.Unit, Callable[[], pint.Unit]],
    convert: bool = False,
) -> pint.Quantity:
    """Ensure that a value is wrapped in a Pint quantity container.

    :param value: Value to ensure the wrapping of.
    :param default_units: Units to use to initialise the :class:`pint.Quantity`
        if ``value`` is not a :class:`pint.Quantity`. A callable can be passed;
        in this case, the applied units will be ``default_units()``.
    :param convert: If ``True``, ``value`` will also be converted to
        ``default_units`` if it is a :class:`pint.Quantity`.
    :returns:
        Converted ``value``.
    """
    if callable(default_units):
        units = default_units()
    else:
        units = default_units

    if not isinstance(units, pint.Unit):
        raise TypeError(
            "Argument 'units' must be a pint.Units or a callable returning "
            "a pint.Units."
        )

    if isinstance(value, pint.Quantity):
        if convert:
            return value.to(units)
        else:
            return value
    else:
        return value * units


def identity(value: Any) -> Any:
    """
    Do nothing and return the value it is passed.

    :param value: Value to apply converter to.
    """
    return value


def to_units(
    units: Union[pint.Unit, Callable[[], pint.Unit]]
) -> Callable[[Any], pint.Quantity]:
    """
    Create a callable ``f(x)`` returning
    :func:`ensure_units(x, units, convert=False) <ensure_units>`.

    :param units: Units to ensure conversion to.
    """

    def f(x):
        return ensure_units(x, units)

    return f
