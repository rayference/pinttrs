import pint


def ensure_units(value, default_units, convert=False):
    """Ensure that a value is wrapped in a Pint quantity container.

    Parameter ``value``:
        Value to ensure the wrapping of.

    Parameter ``default_units`` (callable or :class:`pint.Units`):
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
        default_units = default_units()

    if isinstance(value, pint.Quantity):
        if convert:
            return value.to(default_units)
        else:
            return value
    else:
        return value * default_units
