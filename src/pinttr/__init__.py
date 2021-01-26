from . import converters, exceptions, util, validators
from ._make import attrib


# Package metadata
__version__ = "0.1.0-dev1"
__copyright__ = "Copyright (c) 2021 Vincent Leroy"

# Other definitions
ib = attrib
__all__ = ["attrib", "ib", "converters", "exceptions", "util", "validators"]
