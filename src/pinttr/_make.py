import attr
import pint
from attr import NOTHING

from ._metadata import MetadataKey
from .converters import ensure_units
from .validators import has_compatible_units


def attrib(
    default=NOTHING,
    validator=NOTHING,
    repr=True,
    cmp=None,
    hash=None,
    init=True,
    metadata=None,
    type=None,
    converter=NOTHING,
    factory=None,
    kw_only=False,
    eq=None,
    order=None,
    on_setattr=NOTHING,
    units=NOTHING,
):
    """
    Create a new attribute on a class.
    """

    # Initialise attr.ib arguments
    metadata = dict() if not metadata else metadata

    # Process declared compatible units
    if units is not NOTHING:
        # Set field metadata
        if callable(units) and isinstance(units(), pint.Unit):
            units_callable = units
        
        elif isinstance(units, pint.Unit):
            def units_callable():
                return units

        else:
            raise TypeError(
                "Argument 'units' must be a pint.Units or a callable returning "
                "a pint.Units."
            )

        metadata[MetadataKey.UNITS] = units_callable

        # Set field converter
        if converter is NOTHING:

            def to_units(x):
                return ensure_units(x, units_callable)

            if default is None:
                converter = attr.converters.optional(to_units)
            else:
                converter = to_units

        # Set field validator
        if validator is NOTHING:
            if default is None:
                validator = attr.validators.optional(has_compatible_units)
            else:
                validator = has_compatible_units

        # Ensure that unit conversion and validation is carried out upon setting
        if on_setattr is NOTHING:
            on_setattr = attr.setters.pipe(
                attr.setters.convert, attr.setters.validate
            )

    # If on_setattr hasn't been set because units_compatible is unset, we set it
    # to a valid value
    if on_setattr is NOTHING:
        on_setattr = None

    return attr.ib(
        default=default,
        validator=validator,
        repr=repr,
        cmp=cmp,
        hash=hash,
        init=init,
        metadata=metadata,
        type=type,
        converter=converter,
        factory=factory,
        kw_only=kw_only,
        eq=eq,
        order=order,
        on_setattr=on_setattr,
    )
