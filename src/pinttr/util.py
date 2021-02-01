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


def units_compatible(unit1: pint.Unit, unit2: pint.Unit) -> bool:
    """
    Check if two units are compatible. Accounts for angle units.

    :param unit1: First unit to check for compatibility.
    :param unit2: Second unit to check for compatibility.
    :returns: ``True`` if ``unit1`` and ``unit2`` have the same dimensionality,
        ``False`` otherwise.
    """
    return (1.0 * unit1 / unit2).unitless
