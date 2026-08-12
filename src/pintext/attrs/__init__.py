"""
*attrs* integration.

Requires the ``attrs`` extra::

    pip install "pintext[attrs]"
"""

try:
    import attrs as _attrs  # noqa: F401
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "pintext.attrs requires the 'attrs' extra: pip install 'pintext[attrs]'"
    ) from e

from ._field import field
from ._metadata import MetadataKey
from ._validators import has_compatible_units

__all__ = ["MetadataKey", "field", "has_compatible_units"]
