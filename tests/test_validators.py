import attr
import pint
import pytest

import pinttr
from pinttr.exceptions import UnitsError
from pinttr.validators import has_compatible_units


def test_has_compatible_units():
    """
    Unit tests for :func:`pinttr.validators.has_compatible_units`.
    """
    ureg = pint.UnitRegistry()

    @attr.s
    class MyClass:
        length = pinttr.ib(
            default=0.0 * ureg.m,
            units=ureg.m,
            validator=has_compatible_units,
            converter=None,
        )
        angle = pinttr.ib(
            default=0.0 * ureg.deg,
            units=ureg.deg,
            validator=has_compatible_units,
            converter=None,
        )

    # Validation passes if units have the same dimensionality
    MyClass(length=1.0 * ureg.km)
    MyClass(length=1.0 * ureg.mile)
    MyClass(angle=1.0 * ureg.rad)

    # Validation fails even if units have the same dimensionality but represent different quantities
    with pytest.raises(UnitsError):
        MyClass(angle=1.0 * ureg.dimensionless)

    # Validation fails if value has no units
    with pytest.raises(UnitsError):
        MyClass(angle=1.0)
