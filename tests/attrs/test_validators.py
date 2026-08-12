import attrs
import pint
import pytest

from pintext.attrs import field, has_compatible_units
from pintext.exceptions import UnitsError


class TestHasCompatibleUnits:
    def test_main(self):
        """
        Unit tests for :func:`pintext.attrs.has_compatible_units`.
        """
        ureg = pint.UnitRegistry()

        @attrs.define
        class MyClass:
            length = field(
                default=0.0 * ureg.m,
                units=ureg.m,
                validator=has_compatible_units,
                converter=None,
            )
            angle = field(
                default=0.0 * ureg.deg,
                units=ureg.deg,
                validator=has_compatible_units,
                converter=None,
            )

        # Validation passes if units have the same dimensionality
        MyClass(length=1.0 * ureg.km)
        MyClass(length=1.0 * ureg.mile)
        MyClass(angle=1.0 * ureg.rad)

        # Validation fails even if units have the same dimensionality but represent
        # different quantities
        with pytest.raises(UnitsError):
            MyClass(angle=1.0 * ureg.dimensionless)

        # Validation fails if value has no units
        with pytest.raises(UnitsError):
            MyClass(angle=1.0)

    def test_reports_field_name(self):
        """
        The validator reports the name of the offending field.
        """
        ureg = pint.UnitRegistry()

        @attrs.define
        class MyClass:
            length = field(default=0.0 * ureg.m, units=ureg.m, converter=None)

        with pytest.raises(UnitsError, match="field 'length'"):
            MyClass(length=1.0 * ureg.s)
