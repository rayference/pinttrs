from typing import Any, Callable, Union

import pint

from ._generator import UnitGenerator
from .util import ensure_units


def to_units(units: Union[pint.Unit, UnitGenerator]) -> Callable[[Any], pint.Quantity]:
    """
    Create a callable ``f(x)`` returning
    :func:`ensure_units(x, units, convert=False) <ensure_units>`.

    :param units:
        Units to ensure conversion to.
    """

    def f(x):
        return ensure_units(x, units)

    return f
