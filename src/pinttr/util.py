from copy import copy


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


def interpret_units(d, ureg, inplace=False):
    """
    Interpret units in a dictionary. The dictionary is searched for matching
    magnitude-units field pairs. For a magnitude field with key ``"x"``, the
    corresponding unit field is ``"x_units"``. For each pair found, the 
    magnitude field is attached units and converted to a :class:`pint.Quantity`
    object. The unit field is then dropped.

    .. admonition:: Example

       .. code-block:: python
          
          {
              "field": 1.0,
              "field_units": "m"
          }

       will be interpreted as

       .. code-block:: python
          
          {"field": ureg.Quantity(1.0, "m")}

    .. warning:: 

       * Dictionary keys must be strings.

    :param d:
        Dictionary in which units we be interpreted.

    :type d:
        :class:`dict`

    :param ureg:
        Unit registry to use for unit creation.

    :type ureg:
        :class:`pint.UnitRegistry`

    :param inplace:
        If ``True``, modify the dictionary in-place; otherwise, return a 
        modified copy.
    
    :type inplace:
        :class:`bool`

    :returns:
        A copy of ``d``, where unit fields are interpreted using ``ureg`` to 
        attach units to the corresponding magnitude field.

    :rtype:
        :class:`dict`

    """
    if not inplace:
        result = copy(d)
    else:
        result = d

    for key in list(result.keys()):
        if key.endswith("_units"):
            magnitude_key = key[:-6]
            try:
                result[magnitude_key] = ureg.Quantity(result[magnitude_key], result[key])
                del result[key]
            except KeyError:
                continue

    return result


def units_compatible(unit1, unit2):
    """
    Check if two units are compatible. Accounts for angle units.

    :param unit1:
        First unit to check for compatibility.

    :type unit1:
        :class:`pint.Unit`

    :param unit2:
        Second unit to check for compatibility.

    :type unit2:
        :class:`pint.Unit`

    :returns:
        ``True`` if ``unit1`` and ``unit2`` have the same dimensionality,
        ``False`` otherwise.

    :rtype:
        :class:`bool`
    """
    return (1.0 * unit1 / unit2).unitless
