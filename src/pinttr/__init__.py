"""
Pinttrs package.

Pint meets attrs.
"""


from . import converters, exceptions, util, validators
from ._context import UnitContext
from ._defaults import get_unit_registry, set_unit_registry
from ._generator import UnitGenerator
from ._interpret import interpret_units
from ._make import attrib
from ._next_gen import field

# Package metadata
from ._version import version as __version__

# Other definitions
ib = attrib
__all__ = [
    "UnitContext",
    "UnitGenerator",
    "attrib",
    "converters",
    "exceptions",
    "field",
    "get_unit_registry",
    "ib",
    "interpret_units",
    "set_unit_registry",
    "util",
    "validators",
]
