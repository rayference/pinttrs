import pint

from pinttr.util import *

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


def test_interpret_units():
    """
    Unit tests for :func:`pinttrs.util.interpret_units`.
    """
    # A unit registry is required
    ureg = pint.UnitRegistry()

    # fmt: off
    # Normal operation: units are applied and the '_units' field is removed
    assert interpret_units({
        "a": 1.0,
        "a_units": "m"
    }, ureg) == {
        "a": 1.0 * ureg.m
    }
    # Also works if the key of the magnitude field is an empty string
    assert interpret_units({
        "": 1.0,
        "_units": "m"
    }, ureg) == {
        "": 1.0 * ureg.m
    }
    # Also works if the magnitude field key is '_units'
    assert interpret_units({
        "_units": 1.0,
        "_units_units": "m"
    }, ureg) == {
        "_units": 1.0 * ureg.m
    }

    # If a unit field has no associated magnitude, nothing changes
    assert interpret_units({"a_units": 1.,}, ureg) == {"a_units": 1.}
    assert interpret_units({"_units": "m",}, ureg) == {"_units": "m"}
    # fmt: on

    # If inplace is False, the dict is not modified
    d = {"a": 1.0, "a_units": "m"}
    assert interpret_units(d, ureg) != d
    # If inplace is True, the dict is modified
    interpret_units(d, ureg, inplace=True)
    assert d == {"a": 1.0 * ureg.m}


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
