import pint

from pinttr.util import always_iterable, units_compatible

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
