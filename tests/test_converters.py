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


def test_to_quantity_xarray():
    """Test conversion of xarray DataArray to Pint quantities."""
    xr = pytest.importorskip("xarray")
    import numpy as np

    # DataArray with units attribute is converted
    data = xr.DataArray([1.0, 2.0, 3.0], attrs={"units": "m"})
    result = to_quantity(data)
    assert isinstance(result, ureg.Quantity)
    assert np.array_equal(result.magnitude, np.array([1.0, 2.0, 3.0]))
    assert result.units == ureg.m

    # DataArray without units attribute is passed through
    data_no_units = xr.DataArray([1.0, 2.0, 3.0])
    result_no_units = to_quantity(data_no_units)
    assert isinstance(result_no_units, xr.DataArray)
    assert result_no_units is data_no_units

    # DataArray with empty attrs dict is passed through
    data_empty_attrs = xr.DataArray([1.0, 2.0, 3.0], attrs={})
    result_empty_attrs = to_quantity(data_empty_attrs)
    assert isinstance(result_empty_attrs, xr.DataArray)
    assert result_empty_attrs is data_empty_attrs

    # Multi-dimensional DataArray
    data_2d = xr.DataArray([[1.0, 2.0], [3.0, 4.0]], attrs={"units": "km"})
    result_2d = to_quantity(data_2d)
    assert isinstance(result_2d, ureg.Quantity)
    assert np.array_equal(result_2d.magnitude, np.array([[1.0, 2.0], [3.0, 4.0]]))
    assert result_2d.units == ureg.km
