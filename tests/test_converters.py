import pint
import pytest
from pint import DimensionalityError
from pinttr.converters import *

ureg = pint.UnitRegistry()


def test_ensure_units():
    # Units are applied to unitless values
    assert ensure_units(100, ureg.km) == ureg.Quantity(100, "km")
    # Default behaviour does not convert quantity values
    assert ensure_units(ureg.Quantity(100, "m"), ureg.km) == ureg.Quantity(
        100, "m"
    )
    # If a quantity value with incompatible units is passed, does not raise
    ensure_units(ureg.Quantity(100, "m"), ureg.s)

    # If conversion is requested, it is performed
    assert ensure_units(
        ureg.Quantity(100, "m"), ureg.km, convert=True
    ) == ureg.Quantity(0.1, "km")
    # If a quantity value with incompatible units is passed, and conversion is requested raise
    with pytest.raises(DimensionalityError):
        ensure_units(ureg.Quantity(100, "m"), ureg.s, convert=True)

    # If we pass a callable value, it is evaluated
    def f():
        return ureg.km
    assert ensure_units(100, f) == ureg.Quantity(100, "km")
    assert ensure_units(100, lambda: ureg.s) == ureg.Quantity(100, "s")
    