import attrs
import pint
import pinttr
import pytest
from pinttr._metadata import MetadataKey
from pinttr.exceptions import UnitsError

ureg = pint.UnitRegistry()


def test_attrib_metadata():
    """
    Unit tests for :func:`pinttrs._make.attrib` (metadata checks on produced
    attribute specifications).
    """
    # If 'units' argument is not passed, behaviour is similar to that of attr.ib()
    field_no_quantity = pinttr.ib(default=ureg.Quantity(0, "m"))
    assert MetadataKey.UNITS not in field_no_quantity.metadata

    # Units are wrapped into generators and registered as field metadata
    field_distance = pinttr.attrib(units=ureg.m)
    assert field_distance.metadata[MetadataKey.UNITS]() == ureg.m

    field_angle = pinttr.attrib(units=ureg.deg)
    assert field_angle.metadata[MetadataKey.UNITS]() == ureg.deg

    # Units specified with generators  are directly registered as metadata
    ugen = pinttr.UnitGenerator(ureg.m)
    field_distance = pinttr.attrib(units=ugen)
    assert field_distance.metadata[MetadataKey.UNITS]() == ureg.m

    # Units registered with a generator can be overridden
    with ugen.override(ureg.s):
        assert field_distance.metadata[MetadataKey.UNITS]() == ureg.s
    assert field_distance.metadata[MetadataKey.UNITS]() == ureg.m

    # If 'units' argument is not a pint.Unit or a callable returning a pint.Unit, raise
    with pytest.raises(TypeError):
        pinttr.attrib(units="km")


def test_attrib_converter_validator():
    """
    Unit tests for :func:`pinttrs._make.attrib` (converter and validator).
    """
    ugen = pinttr.UnitGenerator(ureg.m)

    # If no converter is defined, automatic unit conversion and validation is added
    @attrs.define
    class MyClass:
        field = pinttr.attrib(default=None, units=ugen)

    # Default set to None makes converter optional
    assert MyClass().field is None
    # Automatic unit conversion is performed
    assert MyClass(1.0).field == 1.0 * ureg.m
    # If a generator was used to fetch units at runtime, updating the conversion units is possible
    ugen.units = ureg.km
    assert MyClass(1.0).field == 1.0 * ureg.km
    # We can even change dimensionality
    ugen.units = ureg.s
    assert MyClass(1.0).field == 1.0 * ureg.s

    # If we use a pint.Quantity to init our field, it should pass if units are compatible
    ugen.units = ureg.m
    assert MyClass(1.0 * ureg.m).field == 1.0 * ureg.m
    # And it should raise if units are not compatible
    ugen.units = ureg.s
    with pytest.raises(UnitsError):
        MyClass(1.0 * ureg.m)

    # With defaults, we should also have automatic conversion and validation upon setting field
    ugen.units = ureg.m
    a = MyClass(1.0)
    assert a.field == 1.0 * ureg.m
    a.field = 1.0 * ureg.km
    assert a.field == 1.0 * ureg.km
    a.field = 1.0
    assert a.field == 1.0 * ureg.m
    with pytest.raises(UnitsError):
        a.field = 1.0 * ureg.s
