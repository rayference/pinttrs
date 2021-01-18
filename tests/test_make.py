import attr
import pint
import pytest

import pinttr
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

    # Units are wrapped into callables and registered as field metadata
    field_distance = pinttr.ib(units=ureg.m)
    assert field_distance.metadata[MetadataKey.UNITS]() == ureg.m

    field_angle = pinttr.ib(units=ureg.deg)
    assert field_angle.metadata[MetadataKey.UNITS]() == ureg.deg

    # Units defined using callables are directly registered as metadata
    dynamic_units = ureg.m
    field_distance = pinttr.ib(units=lambda: dynamic_units)
    assert field_distance.metadata[MetadataKey.UNITS]() == ureg.m

    # Runtime query of units can be achieved
    dynamic_units = ureg.s
    assert field_distance.metadata[MetadataKey.UNITS]() == ureg.s

    # If 'units' argument is not a pint.Unit or a callable returning a pint.Unit, raise
    with pytest.raises(TypeError):
        pinttr.ib(units="km")


def test_attrib_converter_validator():
    """
    Unit tests for :func:`pinttrs._make.attrib` (converter and validator).
    """
    dynamic_units = ureg.m

    # If no converter is defined, automatic unit conversion and validation is added
    @attr.s
    class MyClass:
        field = pinttr.ib(default=None, units=lambda: dynamic_units)

    # Default set to None makes converter optional
    assert MyClass().field is None
    # Automatic unit conversion is performed
    assert MyClass(1.0).field == 1.0 * ureg.m
    # If a callable was used to fetch units at runtime, updating the conversion units is possible
    dynamic_units = ureg.km
    assert MyClass(1.0).field == 1.0 * ureg.km
    # We can even change dimensionality
    dynamic_units = ureg.s
    assert MyClass(1.0).field == 1.0 * ureg.s

    # If we use a pint.Quantity to init our field, it should pass if units are compatible
    dynamic_units = ureg.m
    assert MyClass(1.0 * ureg.m).field == 1.0 * ureg.m
    # And it should raise if units are not compatible
    dynamic_units = ureg.s
    with pytest.raises(UnitsError):
        MyClass(1.0 * ureg.m).field

    # With defaults, we should also have automatic conversion and validation upon setting field
    dynamic_units = ureg.m
    a = MyClass(1.0)
    assert a.field == 1.0 * ureg.m
    a.field = 1.0 * ureg.km
    assert a.field == 1.0 * ureg.km
    a.field = 1.0
    assert a.field == 1.0 * ureg.m
    with pytest.raises(UnitsError):
        a.field = 1.0 * ureg.s

    # # -- This also tests if bound class methods return the expected value
    # assert MyClass._fields_supporting_units() == (
    #     "field_distance",
    #     "field_angle",
    #     "field_no_quantity",
    # )

    # assert MyClass._fields_compatible_units() == {
    #     "field_distance": ureg.m,
    #     "field_angle": ureg.deg,
    # }

    # # Check if converters are correctly set
    # @unit_enabled
    # @attr.s
    # class MyClass:
    #     field_no_quantity = attrib_quantity(default=ureg.Quantity(100, "km"))

    #     field_no_converter = attrib_quantity(
    #         default=ureg.Quantity(100, "km"),
    #         units_compatible=ureg.m,
    #         units_add_converter=False,
    #         units_add_validator=False,
    #     )

    #     field_static_converter = attrib_quantity(
    #         default=ureg.Quantity(100, "km"),
    #         units_compatible=ureg.m,
    #         units_add_converter=True,
    #         units_add_validator=False,
    #     )

    #     field_dynamic_converter = attrib_quantity(
    #         default=ureg.Quantity(100, "km"),
    #         units_compatible=cdu.generator("length"),
    #         units_add_converter=True,
    #         units_add_validator=False,
    #     )

    # # -- Whatever the conversion policy, quantities used to init the object should
    # #    be left intact
    # with cdu.override({"length": ureg.m}):
    #     o = MyClass()
    # assert o.field_no_quantity == ureg.Quantity(100, "km")
    # assert o.field_no_quantity.units == ureg.km
    # assert o.field_no_converter == ureg.Quantity(100, "km")
    # assert o.field_no_converter.units == ureg.km
    # assert o.field_static_converter == ureg.Quantity(100, "km")
    # assert o.field_static_converter.units == ureg.km
    # assert o.field_dynamic_converter == ureg.Quantity(100, "km")
    # assert o.field_dynamic_converter.units == ureg.km
    # # -- Converters should add units to non-quantity values
    # with cdu.override({"length": ureg.km}):
    #     o = MyClass(
    #         field_no_quantity=100,
    #         field_no_converter=100,
    #         field_static_converter=100,
    #         field_dynamic_converter=100,
    #     )
    # assert o.field_no_quantity == 100
    # assert o.field_no_converter == 100
    # assert o.field_static_converter == ureg.Quantity(100, "m")
    # assert o.field_dynamic_converter == ureg.Quantity(100, "km")

    # # -- Check if validators are correctly set
    # @unit_enabled
    # @attr.s
    # class MyClass:
    #     field_no_quantity = attrib_quantity(default=ureg.Quantity(100, "km"))

    #     field_no_validator = attrib_quantity(
    #         default=ureg.Quantity(100, "km"),
    #         units_compatible=ureg.m,
    #         units_add_converter=True,
    #         units_add_validator=False,
    #     )

    #     field_unit_validator = attrib_quantity(
    #         default=ureg.Quantity(100, "km"),
    #         units_compatible=ureg.m,
    #         units_add_converter=True,
    #         units_add_validator=True,
    #     )

    #     field_multi_validator = attrib_quantity(
    #         default=ureg.Quantity([1, 1, 1], "km"),
    #         validator=validator_has_len(3),
    #         units_compatible=ureg.m,
    #         units_add_converter=True,
    #         units_add_validator=True,
    #     )

    # o = MyClass()
    # # -- We assume that on_setattr is set to execute converters and
    # #    validators (this also tests that part of attrib_quantity())
    # o.field_no_quantity = 100
    # assert o.field_no_quantity == 100

    # o.field_no_validator = ureg.Quantity(100, "s")  # Should not fail
    # with pytest.raises(UnitsError):  # Incompatible dimensions
    #     o.field_unit_validator = ureg.Quantity(100, "s")
    # with pytest.raises(UnitsError):  # Compatible dimensions, incompatible units
    #     o.field_unit_validator = ureg.Quantity(100, "m/deg")

    # o.field_multi_validator = ureg.Quantity([1, 1, 1], "m")  # Should not fail
    # with pytest.raises(UnitsError):  # Wrong unit
    #     o.field_multi_validator = ureg.Quantity([1, 1, 1], "m/deg")
    # with pytest.raises(ValueError):  # Wrong size
    #     o.field_multi_validator = ureg.Quantity([0, 0], "m")
    # with pytest.raises(ValueError):  # Wrong and unit (unit is validated last)
    #     o.field_multi_validator = ureg.Quantity([0, 0], "s")

    # # None default support
    # # -- Check that field with None default behaves as expected
    # @unit_enabled
    # @attr.s
    # class MyClass:
    #     field = attrib_quantity(
    #         default=None,
    #         converter=attr.converters.optional(converter_quantity(float)),
    #         units_compatible=ureg.m,
    #     )

    # o = MyClass()
    # o = MyClass(ureg.Quantity(1.0, "m"))
    # o.field = None
    # assert o.field is None
    # o.field = 1.0
    # assert o.field == ureg.Quantity(1.0, "m")
    # o.field = ureg.Quantity(1.0, "m")
    # assert o.field == ureg.Quantity(1.0, "m")
    # with pytest.raises(ValueError):
    #     o.field = "a"
