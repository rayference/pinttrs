import pint

#: Default unit registry. Unless modified with :func:`.set_unit_registry`, it is
#: Pint's `application registry
#: <https://pint.readthedocs.io/en/stable/getting/pint-in-your-projects.html#having-a-shared-registry>`__.
unit_registry = pint.get_application_registry()


def set_unit_registry(ureg: pint.UnitRegistry | pint.ApplicationRegistry) -> None:
    """
    Set the default unit registry. By default, Pintext uses the
    `application registry <https://pint.readthedocs.io/en/stable/getting/pint-in-your-projects.html#having-a-shared-registry>`__.

    :param ureg: Unit registry.
    :raises: :class:`TypeError` if ``ureg`` is not a :class:`pint.UnitRegistry`.
    """
    global unit_registry
    if not isinstance(ureg, (pint.UnitRegistry, pint.ApplicationRegistry)):
        raise TypeError(
            "ureg must be a pint.UnitRegistry or pint.ApplicationRegistry instance"
        )
    unit_registry = ureg


def get_unit_registry() -> pint.UnitRegistry | pint.ApplicationRegistry:
    """
    Get the default unit registry. By default, Pintext uses the
    `application registry <https://pint.readthedocs.io/en/stable/getting/pint-in-your-projects.html#having-a-shared-registry>`__.

    :returns: The registry currently used as a default by Pintext.
    """
    return unit_registry
