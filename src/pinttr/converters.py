import pint


def ensure_units(value, default_units, convert=False):
    """Ensure that a value is wrapped in a Pint quantity container.

    Parameter ``value``:
        Value to ensure the wrapping of.

    Parameter ``default_units`` (callable or :class:`pint.Unit`):
        Units to use to initialise the :class:`pint.Quantity` if value is not
        a :class:`pint.Quantity`. A callable can be passed; in this case,
        the applied units will be ``default_units()``.

    Parameter ``convert`` (bool):
        If ``True``, ``value`` will also be converted to ``default_units`` if
        it is a :class:`pint.Quantity`.

    Returns → :class:`pint.Quantity`:
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


def to_units(units):
    """
    Create a callable ``f(x)`` returning
    :func:`ensure_units(x, units) <ensure_units>`.
    """

    def f(x):
        return ensure_units(x, units)

    return f
