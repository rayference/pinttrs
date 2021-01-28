import pint


def ensure_units(value, default_units, convert=False):
    """Ensure that a value is wrapped in a Pint quantity container.

    :param value:
        Value to ensure the wrapping of.

    :param default_units:
        Units to use to initialise the :class:`pint.Quantity` if value is not
        a :class:`pint.Quantity`. A callable can be passed; in this case,
        the applied units will be ``default_units()``.

    :type default_units:
        :class:`pint.Unit` or callable

    :param convert:
        If ``True``, ``value`` will also be converted to ``default_units`` if
        it is a :class:`pint.Quantity`.

    :type convert:
        bool

    :returns:
        Converted ``value``.

    :rtype:
         :class:`pint.Quantity`
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


def identity(value):
    """
    Do nothing and return the value it is passed.
    """
    return value


def to_units(units):
    """
    Create a callable ``f(x)`` returning
    :func:`ensure_units(x, units) <ensure_units>`.

    :param units:
        Units to ensure conversion to.

    :type units:
        :class:`pint.Unit` or callable

    :rtype:
        callable
    """

    def f(x):
        return ensure_units(x, units)

    return f
