import enum

import pytest

import pinttr
from pinttr import UnitContext, UnitGenerator

ureg = pinttr.get_unit_registry()


class PhysicalQuantity(enum.Enum):
    LENGTH = "length"
    SPEED = "speed"
    TIME = "time"


def test_unit_context_init():
    """
    Unit tests for :meth:`pinttr._context.UnitContext()`.
    """
    # Empty initialization doesn't raise
    UnitContext()

    # Init from str: UnitGenerator map
    unit_context = UnitContext({"length": UnitGenerator(ureg.m)})
    assert unit_context.registry == {"length": UnitGenerator(ureg.m)}

    # Init from str: Unit map
    unit_context = UnitContext({"length": ureg.m})
    assert unit_context.registry == {"length": UnitGenerator(ureg.m)}

    # Init from str: str map
    unit_context = UnitContext({"length": "m"}, interpret_str=True)
    assert unit_context.registry == {"length": UnitGenerator(ureg.m)}

    # Init from str: str map: fails if interpret_str is not True
    with pytest.raises(TypeError):
        UnitContext({"length": "m"})

    # Init from Enum: UnitGenerator map
    unit_context = UnitContext(
        {"length": UnitGenerator(ureg.m)}, key_converter=PhysicalQuantity
    )
    assert unit_context.registry == {PhysicalQuantity.LENGTH: UnitGenerator(ureg.m)}

    # Init fails if dict values are not str, pint.Unit or UnitGenerator
    with pytest.raises(TypeError):
        UnitContext({"length": 1.0})


def test_unit_context_getters():
    # Unit generators are evaluated
    unit_context = UnitContext(
        {"length": ureg.m, "time": ureg.s}, key_converter=PhysicalQuantity
    )
    assert unit_context.get("length") == ureg.m
    assert unit_context.get("time") == ureg.s

    # Square brackets can be used to access the getter
    assert unit_context["length"] == unit_context.get("length")
    assert unit_context["time"] == unit_context.get("time")

    # Raise if key is unregistered
    with pytest.raises(KeyError):
        unit_context.get("speed")  # Still, the key must pass conversion

    # More complex unit generators are also evaluated
    unit_context.register(
        "speed",
        UnitGenerator(lambda: unit_context.get("length") / unit_context.get("time")),
    )
    assert unit_context.get("speed") == ureg.m / ureg.s

    # Dictionary expansion returns correct keys and values
    assert unit_context.get_all() == {
        PhysicalQuantity.LENGTH: ureg.m,
        PhysicalQuantity.TIME: ureg.s,
        PhysicalQuantity.SPEED: ureg.m / ureg.s,
    }

    # Square brackets can be used as an alias to register()
    unit_context["length"] = ureg.km
    assert unit_context.get("length") == ureg.km


def test_unit_context_override():
    unit_context = UnitContext(key_converter=PhysicalQuantity)
    unit_context.update(
        {
            "length": ureg.m,
            "time": ureg.s,
            "speed": UnitGenerator(
                lambda: unit_context.get("length") / unit_context.get("time")
            ),
        }
    )

    # Override with dict propagates to stored generators
    with unit_context.override(
        {PhysicalQuantity.LENGTH: ureg.km, PhysicalQuantity.TIME: ureg.h}
    ):
        assert unit_context.get("length") == ureg.km
        assert unit_context.get("time") == ureg.h
        assert unit_context.get("speed") == ureg.Unit("km/h")
    assert unit_context.get("length") == ureg.m
    assert unit_context.get("time") == ureg.s
    assert unit_context.get("speed") == ureg.Unit("m/s")

    # Override with kwargs behaves similarly
    with unit_context.override(length="km", time="h"):
        assert unit_context.get("length") == ureg.km
        assert unit_context.get("time") == ureg.h
        assert unit_context.get("speed") == ureg.Unit("km/h")
    assert unit_context.get("length") == ureg.m
    assert unit_context.get("time") == ureg.s
    assert unit_context.get("speed") == ureg.Unit("m/s")

    # Override with something else than a dict or kwargs fails
    with pytest.raises(TypeError):
        with unit_context.override(1.0):
            pass


def test_unit_context_deferred():
    unit_context = UnitContext(key_converter=PhysicalQuantity)
    unit_context.update(
        {
            "length": ureg.m,
            "time": ureg.s,
            "speed": UnitGenerator(
                lambda: unit_context.get("length") / unit_context.get("time")
            ),
        }
    )

    # deferred() returns a fully functioning UnitGenerator
    ugen = unit_context.deferred("speed")
    assert isinstance(ugen, UnitGenerator)
    with unit_context.override(length="km", time="s"):
        assert ugen() == ureg("km/s")
