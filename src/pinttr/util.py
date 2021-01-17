def always_iterable(obj, base_type=(str, bytes)):
    """Ensures that the object it is passed is iterable.

    - If ``obj`` is iterable, return an iterator over its items.
    - If ``obj`` is not iterable, return a one-item iterable containing ``obj``.
    - If ``obj`` is `None`, return an empty iterable.

    .. note::

        Copied from the more-itertools library
        [https://github.com/more-itertools].
    """
    if obj is None:
        return iter(())

    if (base_type is not None) and isinstance(obj, base_type):
        return iter((obj,))

    try:
        return iter(obj)
    except TypeError:
        return iter((obj,))


def units_compatible(unit1, unit2):
    """Check if two units are compatible. Accounts for angle units.

    Parameter ``unit1`` (:class:`pint.Unit`):
        First unit to check for compatibility.

    Parameter ``unit2`` (:class:`pint.Unit`):
        Second unit to check for compatibility.

    Returns → bool
        ``True`` if ``unit1`` and ``unit2`` have the same dimensionality,
        ``False`` otherwise.
    """
    return (1.0 * unit1 / unit2).unitless
