from ._metadata import MetadataKey
from .exceptions import UnitsError
from .util import units_compatible


def has_compatible_units(instance, attribute, value):
    """Validates if ``value`` has units compatible with ``attribute``. Only
    works with unit-enabled fields created with :func:`attrib_quantity`."""

    compatible_units = attribute.metadata[MetadataKey.UNITS]()

    try:
        if not units_compatible(value.units, compatible_units):
            raise UnitsError(
                units1=value.units,
                units2=compatible_units,
                extra_msg=f": incompatible units '{value.units}' "
                f"used to set field '{attribute.name}' "
                f"(allowed: '{compatible_units}').",
            )

    except AttributeError:  # value.units doesn't exist
        raise UnitsError(
            units1=None,
            units2=compatible_units,
            extra_msg=f": unitless value '{value}' "
            f"used to set field '{attribute.name}' "
            f"(requires units '{compatible_units}').",
        )
