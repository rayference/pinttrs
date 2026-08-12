"""
Pintext package.

Unit contexts for Pint.
"""

from . import converters, exceptions, util
from ._context import UnitContext
from ._generator import UnitGenerator
from ._registry import get_unit_registry, set_unit_registry

# Package metadata
from ._version import version as __version__
from .converters import ensure_units, to_quantity
from .exceptions import UnitsError
from .util import check_units, units_compatible

__all__ = [
    "UnitContext",
    "UnitGenerator",
    "UnitsError",
    "__version__",
    "check_units",
    "converters",
    "ensure_units",
    "exceptions",
    "get_unit_registry",
    "set_unit_registry",
    "to_quantity",
    "units_compatible",
    "util",
]
