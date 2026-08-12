import pint
import pytest

import pintext


def test_set_unit_registry():
    """
    Unit tests for :func:`pintext._interpret.interpret_units`.
    """
    # The default unit registry is the application registry.
    assert isinstance(pintext.get_unit_registry(), pint.ApplicationRegistry)
    ureg = pint.UnitRegistry()
    assert ureg is not pintext.get_unit_registry()

    # We can change it to the value we like
    pintext.set_unit_registry(ureg)
    assert ureg is pintext.get_unit_registry()

    # But it must be a pint.UnitRegistry
    with pytest.raises(TypeError):
        pintext.set_unit_registry(None)
