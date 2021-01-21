import attr
import pint
from attr import NOTHING

from ._metadata import MetadataKey
from .converters import to_units
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
    Create a new attribute on a class, possibly with units. This function
    wraps :func:`attr.ib` and retains its behaviour unless otherwise specified.

    :param validator:
        If set to :class:`~attr.NOTHING` and ``units`` is not ``None``, defaults
        to :func:`~pinttr.validators.has_compatible_units` (possibly wrapped in
        :func:`attr.validators.optional` if ``default`` is ``None``).
        Otherwise retains original behaviour.

    :param converter:
        If set to :class:`~attr.NOTHING` and ``units`` is not ``None``, defaults
        to :func:`to_units(units) <pinttr.converters.to_units>`
        (possibly wrapped in :func:`attr.converters.optional` if ``default`` is
        ``None``). Otherwise retains original behaviour.

    :param on_setattr:
        If set to :class:`~attr.NOTHING` and ``units`` is not ``None``,
        defaults to
        ``attr.setters.pipe(attr.setters.convert, attr.setters.validate)``.
        Otherwise retains original behaviour.

    :param units:
        Default units attached to the defined attribute.

    :type units:
        :class:`pint.Unit` or callable
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
            if default is None:
                converter = attr.converters.optional(to_units(units_callable))
            else:
                converter = to_units(units_callable)

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

    # If one of the following hasn't been set because units is unset, we set it
    # to the original default value
    if converter is NOTHING:
        converter = None
    if validator is NOTHING:
        validator = None
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
