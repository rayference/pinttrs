import enum

import pinttr
from pinttr._context import UnitContext, UnitGenerator

ureg = pinttr.get_unit_registry()


class PhysicalQuantity(enum.Enum):
    LENGTH = "length"
    SPEED = "speed"
    TIME = "time"


def test_unit_generator():
    # Calling it returns its registered units
    g_length = UnitGenerator(ureg.m)
    assert g_length() == ureg.m

    # Changing its internal state updates returned units
    g_length.units = ureg.km
    assert g_length() == ureg.km

    # We can nest them
    g_length.units = ureg.m
    g_time = UnitGenerator(ureg.s)
    g_speed = UnitGenerator(lambda: g_length() / g_time())
    assert g_speed() == ureg.m / ureg.s

    # Nested generators also update dynamically
    g_length.units = ureg.km
    assert g_speed() == ureg.km / ureg.s

    # Override temporarily updates the internal units
    g_length.units = ureg.m
    with g_length.override(ureg.km):
        assert g_length() == ureg.km
        assert g_speed() == ureg.km / ureg.s
    assert g_length() == ureg.m
    assert g_speed() == ureg.m / ureg.s

    # Also works with strings
    g_length.units = ureg.m
    with g_length.override("km"):
        assert g_length() == ureg.km
        assert g_speed() == ureg.km / ureg.s
    assert g_length() == ureg.m
    assert g_speed() == ureg.m / ureg.s

    # Also works with callables
    with g_length.override(ureg.km), g_speed.override(ureg.mile / ureg.hour):
        assert g_speed() == ureg.mile / ureg.hour
        assert g_length() == ureg.km
    assert g_speed() == ureg.m / ureg.s
    assert g_length() == ureg.m


def test_unit_context_init():
    """
    Unit tests for :meth:`pinttr._context.UnitContext()`.
    """
    # Empty initialisation doesn't raise
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

    # Init from Enum: UnitGenerator map
    unit_context = UnitContext({"length": UnitGenerator(ureg.m)}, key_converter=PhysicalQuantity)
    assert unit_context.registry == {PhysicalQuantity.LENGTH: UnitGenerator(ureg.m)}


def test_unit_context_getters():
    # Unit generators are evaluated
    unit_context = UnitContext(
        {"length": ureg.m, "time": ureg.s},
        key_converter=PhysicalQuantity
    )
    assert unit_context.get("length") == ureg.m
    assert unit_context.get("time") == ureg.s

    # More complex unit generators are also evaluated
    unit_context.register(
        "speed",
        UnitGenerator(lambda: unit_context.get("length") / unit_context.get("time"))
    )
    assert unit_context.get("speed") == ureg.m / ureg.s

    # Dictionary expansion returns correct keys and values
    assert unit_context.get_all() == {
        PhysicalQuantity.LENGTH: ureg.m,
        PhysicalQuantity.TIME: ureg.s,
        PhysicalQuantity.SPEED: ureg.m / ureg.s,
    }


def test_unit_context_override():
    unit_context = UnitContext(key_converter=PhysicalQuantity)
    unit_context.update({
        "length": ureg.m,
        "time": ureg.s,
        "speed": UnitGenerator(lambda: unit_context.get("length") /
                                       unit_context.get("time"))
    })

    # Override with dict propagates to stored generators
    with unit_context.override({
        PhysicalQuantity.LENGTH: ureg.km,
        PhysicalQuantity.TIME: ureg.h
    }):
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
