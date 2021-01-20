from . import converters, exceptions, util, validators
from ._make import attrib


# Package metadata
__version__ = "0.1.0-dev"
__author__ = "Vincent Leroy"
__email__ = "vincent.leroy@rayference.eu"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2021 Vincent Leroy"
__description__ = "Pint meets attrs"
__url__ = "https://github.com/leroyvn/pinttrs"

# Other definitions
ib = attrib
__all__ = ["attrib", "ib", "converters", "exceptions", "util", "validators"]
