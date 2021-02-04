import pytest
from pint import DimensionalityError

from pinttr.converters import *

ureg = pint.UnitRegistry()


def test_ensure_units():
    """
    Unit tests for :func:`pinttrs.converters.ensure_units`.
    """
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
    # If a quantity value with incompatible units is passed and conversion is requested, raise
    with pytest.raises(DimensionalityError):
        ensure_units(ureg.Quantity(100, "m"), ureg.s, convert=True)

    # If we pass a unit generator, it is evaluated
    u = UnitGenerator(ureg.km)
    assert ensure_units(100, u) == ureg.Quantity(100, "km")
    assert ensure_units(100, UnitGenerator(ureg.s)) == ureg.Quantity(100, "s")

    # If we don't use a pint.Unit or a UnitGenerator to specify units, raise
    with pytest.raises(TypeError):
        ensure_units(100, "km")