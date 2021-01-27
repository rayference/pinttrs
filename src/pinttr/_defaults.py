import pint

#: Default unit registry
unit_registry = pint.UnitRegistry()

def set_unit_registry(ureg):
    """
    Set unit registry. By default, Pinttrs has its own registry.
    """
    global unit_registry
    if not isinstance(ureg, pint.UnitRegistry):
        raise TypeError("ureg must be a pint.UnitRegistry")
    unit_registry = ureg

def get_unit_registry():
    """
    Get default unit registry.
    """
    global unit_registry
    return unit_registry
