import attrs
import pint
import pytest

from pintext import UnitGenerator
from pintext.attrs import MetadataKey, field
from pintext.exceptions import UnitsError

ureg = pint.UnitRegistry()


def test_field_metadata():
    """
    Unit tests for :func:`pintext.attrs.field` (metadata checks on produced
    attribute specifications).
    """
    # If 'units' argument is not passed, behaviour is similar to that of attrs.field()
    field_no_quantity = field(default=ureg.Quantity(0, "m"))
    assert MetadataKey.UNITS not in field_no_quantity.metadata

    # Units are wrapped into generators and registered as field metadata
    field_distance = field(units=ureg.m)
    assert field_distance.metadata[MetadataKey.UNITS]() == ureg.m

    field_angle = field(units=ureg.deg)
    assert field_angle.metadata[MetadataKey.UNITS]() == ureg.deg

    # Units specified with generators are directly registered as metadata
    ugen = UnitGenerator(ureg.m)
    field_distance = field(units=ugen)
    assert field_distance.metadata[MetadataKey.UNITS]() == ureg.m

    # Units registered with a generator can be overridden
    with ugen.override(ureg.s):
        assert field_distance.metadata[MetadataKey.UNITS]() == ureg.s
    assert field_distance.metadata[MetadataKey.UNITS]() == ureg.m

    # If 'units' argument is not a pint.Unit or a callable returning a pint.Unit, raise
    with pytest.raises(TypeError):
        field(units="km")


def test_field_converter_validator():
    """
    Unit tests for :func:`pintext.attrs.field` (converter and validator).
    """
    ugen = UnitGenerator(ureg.m)

    # If no converter is defined, automatic unit conversion and validation is added
    @attrs.define
    class MyClass:
        value = field(default=None, units=ugen)

    # Default set to None makes converter optional
    assert MyClass().value is None
    # Automatic unit conversion is performed
    assert MyClass(1.0).value == 1.0 * ureg.m
    # If a generator was used to fetch units at runtime, updating the
    # conversion units is possible
    ugen.units = ureg.km
    assert MyClass(1.0).value == 1.0 * ureg.km
    # We can even change dimensionality
    ugen.units = ureg.s
    assert MyClass(1.0).value == 1.0 * ureg.s

    # If we use a pint.Quantity to init our field, it should pass if units are
    # compatible
    ugen.units = ureg.m
    assert MyClass(1.0 * ureg.m).value == 1.0 * ureg.m
    # And it should raise if units are not compatible
    ugen.units = ureg.s
    with pytest.raises(UnitsError):
        MyClass(1.0 * ureg.m)

    # With defaults, we should also have automatic conversion and validation
    # upon setting the field
    ugen.units = ureg.m
    a = MyClass(1.0)
    assert a.value == 1.0 * ureg.m
    a.value = 1.0 * ureg.km
    assert a.value == 1.0 * ureg.km
    a.value = 1.0
    assert a.value == 1.0 * ureg.m
    with pytest.raises(UnitsError):
        a.value = 1.0 * ureg.s


def test_field_is_keyword_only():
    """
    :func:`pintext.attrs.field` takes keyword arguments only.
    """
    with pytest.raises(TypeError):
        field(ureg.Quantity(0, "m"))
