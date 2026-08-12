from ._metadata import MetadataKey
from ..util import check_units


def has_compatible_units(instance, attribute, value) -> None:
    """
    Validate if ``value`` has units compatible (in the sense of
    :func:`~pintext.units_compatible`) with ``attribute``.

    This validator checks that a Pint quantity has units compatible with the
    units declared for an attribute. It raises
    :class:`~pintext.exceptions.UnitsError` if the units are incompatible or if
    a unitless value is provided.

    Only works with unit-enabled fields created with
    :func:`pintext.attrs.field`.

    This is a thin adapter around :func:`pintext.check_units`, which holds the
    actual check and is shared with the pydantic integration.

    :param instance:
        The class instance being validated.

    :param attribute:
        The attrs attribute being validated (must have units metadata).

    :param value:
        The value to validate (should be a Pint quantity).

    :raises UnitsError:
        If units are incompatible or if a unitless value is provided.
    """
    check_units(value, attribute.metadata[MetadataKey.UNITS](), name=attribute.name)
