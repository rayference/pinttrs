import pint

import pinttr
from pinttr import interpret_units


def test_interpret_units():
    """
    Unit tests for :func:`pinttrs.interpret_units`.
    """
    # We'll use the default unit registry
    ureg = pinttr.get_unit_registry()

    # fmt: off
    # Normal operation: units are applied and the '_units' field is removed
    assert interpret_units({"a": 1.0,"a_units": "m"}) == {"a": 1.0 * ureg.m}
    # Also works if the key of the magnitude field is an empty string
    assert interpret_units({"": 1.0, "_units": "m"}) == {"": 1.0 * ureg.m}
    # Also works if the magnitude field key is '_units'
    assert interpret_units({
        "_units": 1.0,
        "_units_units": "m"
    }) == {
        "_units": 1.0 * ureg.m
    }

    # If a unit field has no associated magnitude, nothing changes
    assert interpret_units({"a_units": 1.,}) == {"a_units": 1.}
    assert interpret_units({"_units": "m",}) == {"_units": "m"}
    # fmt: on

    # If inplace is False, the dict is not modified
    d = {"a": 1.0, "a_units": "m"}
    assert interpret_units(d) != d
    # If inplace is True, the dict is modified
    interpret_units(d, inplace=True)
    assert d == {"a": 1.0 * ureg.m}
