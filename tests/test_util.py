import pint
import pytest
from pint import DimensionalityError

from pinttr import UnitGenerator
from pinttr.util import always_iterable, ensure_units, units_compatible

ureg = pint.UnitRegistry()


def test_always_iterable():
    """
    Unit tests for :func:`pinttrs.util.always_iterable`.
    More tests on original code [https://github.com/more-itertools].
    """
    # Utility function to check for success
    def is_iterable(value):
        try:
            iter(value)
            return True
        except TypeError:
            return False

    # Non-iterable becomes iterable
    assert is_iterable(always_iterable(1))
    assert is_iterable(always_iterable(None))
    # Iterable remains iterable
    assert is_iterable(always_iterable([1, 1]))
    # String is packed in an iterable
    assert list(always_iterable("abc")) == ["abc"]


def test_units_compatible():
    """
    Unit tests for :func:`pinttrs.util.units_compatible`.
    """
    # Units with the same dimension are compatible
    assert units_compatible(ureg.m, ureg.km)
    assert units_compatible(ureg.m, ureg.mile)
    assert units_compatible(ureg.m / ureg.km, ureg.dimensionless)
    assert units_compatible(ureg.Unit("kg * m/s^2"), ureg.Unit("N"))

    # Exception: angles are not compatible with dimensionless
    assert not units_compatible(ureg.rad, ureg.dimensionless)
    assert not units_compatible(ureg.sr, ureg.dimensionless)
    assert not units_compatible(ureg.sr, ureg.rad)


def test_ensure_units():
    """
    Unit tests for :func:`pinttrs.converters.ensure_units`.
    """
    # Units are applied to unitless values
    assert ensure_units(100, ureg.km) == ureg.Quantity(100, "km")
    # Default behaviour does not convert quantity values
    assert ensure_units(ureg.Quantity(100, "m"), ureg.km) == ureg.Quantity(100, "m")
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