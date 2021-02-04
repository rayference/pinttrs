import pinttr
from pinttr import UnitGenerator

ureg = pinttr.get_unit_registry()


def test_unit_generator():
    """
    Unit tests for :class:`pinttr._generator.UnitGenerator()`.
    """
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

    # Also works if passed a string
    g_length.units = ureg.m
    with g_length.override("km"):
        assert g_length() == ureg.km
        assert g_speed() == ureg.km / ureg.s
    assert g_length() == ureg.m
    assert g_speed() == ureg.m / ureg.s

    # Still works if passing a string to override a composed generator
    with g_speed.override("mile/hour"):
        assert g_speed() == ureg.mile / ureg.hour
    assert g_speed() == ureg.m / ureg.s

    # Also works if passed a generator
    g_length.units = ureg.m
    with g_length.override(g_time):
        assert g_length() == ureg.s
    assert g_length() == ureg.m

    # Also updates generators created from callables
    with g_length.override(ureg.km), g_speed.override(ureg.mile / ureg.hour):
        assert g_speed() == ureg.mile / ureg.hour
        assert g_length() == ureg.km
    assert g_speed() == ureg.m / ureg.s
    assert g_length() == ureg.m
