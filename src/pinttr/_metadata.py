import enum


class MetadataKey(enum.Enum):
    """Attribute metadata keys.

    These Enum values should be used as metadata attribute keys. They are 
    immutable and guarantee that no collision can occur with another piece of 
    code.
    """

    # Units compatible with this field (callable)
    UNITS = 0
