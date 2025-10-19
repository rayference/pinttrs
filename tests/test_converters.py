import pytest

from pinttr import UnitGenerator, get_unit_registry
from pinttr.converters import ensure_units, to_quantity
from pinttr.exceptions import DimensionalityError

ureg = get_unit_registry()


def test_ensure_units_callable():
    # Units are applied to unitless values
    assert ensure_units(100, default_units=ureg.km) == 100 * ureg.km
    # Default behaviour does not convert quantity values
    assert ensure_units(100 * ureg.m, default_units=ureg.km) == 100 * ureg.m
    # If a quantity value with incompatible units is passed, does not raise
    ensure_units(100 * ureg.m, default_units=ureg.s)

    # If conversion is requested, it is performed
    assert (
        ensure_units(100 * ureg.m, default_units=ureg.km, convert=True) == 0.1 * ureg.km
    )
    # If a quantity value with incompatible units is passed and conversion is
    # requested, raise
    with pytest.raises(DimensionalityError):
        ensure_units(100 * ureg.m, default_units=ureg.s, convert=True)

    # If we pass a unit generator, it is evaluated
    u = UnitGenerator(ureg.km)
    assert ensure_units(100, default_units=u) == ureg.Quantity(100, "km")
    assert ensure_units(100, default_units=UnitGenerator(ureg.s)) == ureg.Quantity(
        100, "s"
    )

    # If we don't use a pint.Unit or a UnitGenerator to specify units, raise
    with pytest.raises(TypeError):
        ensure_units(100, default_units="km")


def test_ensure_units_functor():
    c = ensure_units(default_units=ureg.km)
    assert c(100) == 100 * ureg.km
    assert c(100 * ureg.m) == 100 * ureg.m
    assert c(100 * ureg.s) == 100 * ureg.s

    c = ensure_units(default_units=ureg.km, convert=True)
    value = c(100 * ureg.m)
    assert value.m == 0.1
    assert value.u == ureg.km
    with pytest.raises(DimensionalityError):
        c(1 * ureg.s)

    u = UnitGenerator(ureg.km)
    c = ensure_units(default_units=u)
    assert c(100) == 100 * ureg.km

    with pytest.raises(TypeError):
        ensure_units(default_units="km")


def test_to_quantity():
    # Unsupported types are passed through
    assert to_quantity(1.0) == 1.0
    assert to_quantity(1.0 * ureg.m) == 1.0 * ureg.m

    # Correctly formed dicts are converted
    assert to_quantity({"value": 1.0, "units": "m"}) == 1.0 * ureg.m
    assert to_quantity({"magnitude": 1.0, "units": "m"}) == 1.0 * ureg.m
    assert to_quantity({"m": 1.0, "u": "m"}) == 1.0 * ureg.m

    # Excess fields raise
    with pytest.raises(ValueError):
        to_quantity({"m": 1.0, "u": "m", "units": "s"})
