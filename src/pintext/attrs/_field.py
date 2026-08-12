import attrs
import pint
from attrs import NOTHING

from ._metadata import MetadataKey
from ._validators import has_compatible_units
from .._generator import UnitGenerator
from ..converters import ensure_units


def field(
    *,
    default=NOTHING,
    validator=NOTHING,
    repr=NOTHING,
    hash=None,
    init=True,
    metadata=None,
    converter=NOTHING,
    factory=None,
    kw_only=False,
    eq=None,
    order=None,
    on_setattr=NOTHING,
    units: pint.Unit | UnitGenerator | None = None,
):
    """
    Create a new attribute on a class, possibly with units. This function wraps
    :func:`attrs.field` and retains its behaviour unless otherwise specified.

    :param validator:
        If set to :class:`~attrs.NOTHING` and ``units`` is not ``None``,
        defaults to :func:`~pintext.attrs.has_compatible_units` (possibly
        wrapped in :func:`attrs.validators.optional` if ``default`` is
        ``None``). Otherwise retains original behaviour.

    :param repr:
        If set to :class:`~attrs.NOTHING` and ``units`` is not ``None``,
        defaults to a callable printing quantities nicely.
        Otherwise retains original behaviour.

    :param converter:
        If set to :class:`~attrs.NOTHING` and ``units`` is not ``None``,
        defaults to
        :func:`ensure_units(default_units=units) <pintext.converters.ensure_units>`
        (possibly wrapped in :func:`attrs.converters.optional` if ``default`` is
        ``None``). Otherwise retains original behaviour.

    :param on_setattr:
        If set to :class:`~attrs.NOTHING` and ``units`` is not ``None``,
        defaults to
        ``attrs.setters.pipe(attrs.setters.convert, attrs.setters.validate)``.
        Otherwise retains original behaviour.

    :param units:
        Default units attached to the defined attribute. Accepts a
        :class:`~pintext.UnitGenerator` instance. Has no effect if set to
        ``None``.

    .. rubric:: Examples

    >>> @attrs.define
    ... class Sphere:
    ...     radius: pint.Quantity = field(units=ureg.m)
    >>> Sphere(radius=1.0)
    Sphere(radius=1.0 m)
    >>> Sphere(radius=1.0 * ureg.km)
    Sphere(radius=1.0 km)

    Passing a :class:`~pintext.UnitGenerator` (typically obtained from a
    :class:`~pintext.UnitContext`) defers unit evaluation:

    >>> generator = UnitGenerator(ureg.m)
    >>> @attrs.define
    ... class Sphere:
    ...     radius: pint.Quantity = field(units=generator)
    >>> with generator.override(ureg.km):
    ...     Sphere(radius=1.0)
    Sphere(radius=1.0 km)
    """

    # Initialize attrs.field arguments
    metadata = {} if not metadata else metadata

    # Process declared compatible units
    if units is not None:
        # Set field metadata
        if isinstance(units, UnitGenerator):
            unit_generator = units

        elif isinstance(units, pint.Unit):
            unit_generator = UnitGenerator(units)

        else:
            raise TypeError("Argument 'units' must be a pint.Unit or a UnitGenerator")

        metadata[MetadataKey.UNITS] = unit_generator

        # Set field converter
        if converter is NOTHING:
            if default is None:
                converter = attrs.converters.optional(
                    ensure_units(default_units=unit_generator)
                )
            else:
                converter = ensure_units(default_units=unit_generator)

        # Set field validator
        if validator is NOTHING:
            if default is None:
                validator = attrs.validators.optional(has_compatible_units)
            else:
                validator = has_compatible_units

        # Ensure that unit conversion and validation is carried out upon setting
        if on_setattr is NOTHING:
            on_setattr = attrs.setters.pipe(
                attrs.setters.convert, attrs.setters.validate
            )

        # Set field repr
        if repr is NOTHING:

            def f(x):
                if isinstance(x, pint.Quantity):
                    return f"{x:~P}"
                else:
                    return x.__repr__()

            repr = f

    # If one of the following hasn't been set because units is unset, we set it
    # to the original default value
    if converter is NOTHING:
        converter = None
    if validator is NOTHING:
        validator = None
    if on_setattr is NOTHING:
        on_setattr = None
    if repr is NOTHING:
        repr = True

    return attrs.field(
        default=default,
        validator=validator,
        repr=repr,
        hash=hash,
        init=init,
        metadata=metadata,
        converter=converter,
        factory=factory,
        kw_only=kw_only,
        eq=eq,
        order=order,
        on_setattr=on_setattr,
    )
