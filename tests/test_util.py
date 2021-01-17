import pint
from pinttr.util import *

ureg = pint.UnitRegistry()


def test_always_iterable():
    def is_iterable(value):
        try:
            iter(value)
            return True
        except TypeError:
            return False

    assert is_iterable(always_iterable(1))
    assert is_iterable(always_iterable([1, 1]))
    assert is_iterable(always_iterable(None))


def test_units_compatible():
    # Units with the same dimension are compatible
    assert units_compatible(ureg.m, ureg.km)
    assert units_compatible(ureg.m / ureg.km, ureg.dimensionless)
    assert units_compatible(ureg.Unit("kg * m/s^2"), ureg.Unit("N"))

    # Exception: angles are not compatible with dimensionless
    assert not units_compatible(ureg.rad, ureg.dimensionless)
    assert not units_compatible(ureg.sr, ureg.dimensionless)
    assert not units_compatible(ureg.sr, ureg.rad)
