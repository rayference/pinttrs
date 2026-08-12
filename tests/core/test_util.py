import pint
import pytest

from pintext.exceptions import UnitsError
from pintext.util import check_units, units_compatible

ureg = pint.UnitRegistry()


def test_units_compatible():
    """
    Unit tests for :func:`pintext.util.units_compatible`.
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


def test_check_units():
    """
    Unit tests for :func:`pintext.util.check_units`.
    """
    # Compatible units pass
    assert check_units(1.0 * ureg.m, ureg.m) is None
    assert check_units(1.0 * ureg.km, ureg.m) is None

    # Incompatible units raise
    with pytest.raises(UnitsError):
        check_units(1.0 * ureg.s, ureg.m)

    # Unitless values raise
    with pytest.raises(UnitsError):
        check_units(1.0, ureg.m)


def test_check_units_message():
    """
    The field name is reported in the error message when supplied.
    """
    with pytest.raises(UnitsError, match="field 'radius'"):
        check_units(1.0 * ureg.s, ureg.m, name="radius")

    # Without a name, a generic wording is used
    with pytest.raises(UnitsError, match="to set value"):
        check_units(1.0 * ureg.s, ureg.m)
