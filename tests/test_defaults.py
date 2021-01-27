import pint
import pytest

import pinttr


def test_set_unit_registry():
    """
    Unit tests for :func:`pinttr._interpret.interpret_units`.
    """
    # The default unit registry is a pint.UnitRegistry instance
    assert isinstance(pinttr.get_unit_registry(), pint.UnitRegistry)
    ureg = pint.UnitRegistry()
    assert ureg is not pinttr.get_unit_registry()

    # We can change it to the value we like
    pinttr.set_unit_registry(ureg)
    assert ureg is pinttr.get_unit_registry()

    # But it must be a pint.UnitRegistry
    with pytest.raises(TypeError):
        pinttr.set_unit_registry(None)
