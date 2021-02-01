from copy import copy
from typing import Any, Dict, Union

import pint

from ._defaults import get_unit_registry


def interpret_units(
        d: Dict[str, Any],
        ureg: Union[pint.UnitRegistry, None] = None,
        inplace: bool = False,
) -> Dict[str, Any]:
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

    .. warning:: Dictionary keys must be strings.

    :param d: Dictionary in which units will be interpreted.
    :param ureg: Unit registry to use for unit creation. If set to ``None``,
        Pinttrs's registered unit registry is used. See also
        :func:`pinttr.set_unit_registry`.
    :param inplace: If ``True``, modify the dictionary in-place; otherwise,
        return a modified copy.
    :returns: A copy of ``d``, where unit fields are interpreted using ``ureg``
        to attach units to the corresponding magnitude field.
    """
    if ureg is None:
        ureg = get_unit_registry()

    if not inplace:
        result = copy(d)
    else:
        result = d

    for key in list(result.keys()):
        if key.endswith("_units"):
            magnitude_key = key[:-6]
            try:
                result[magnitude_key] = ureg.Quantity(
                    result[magnitude_key], result[key]
                )
                del result[key]
            except KeyError:
                continue

    return result
