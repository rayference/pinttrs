from typing import Union

import pint

#: Default unit registry (if not modified with :func:`.set_unit_registry`, it is the `application registry <https://pint.readthedocs.io/en/stable/getting/pint-in-your-projects.html#having-a-shared-registry>`_).
unit_registry = pint.get_application_registry()


def set_unit_registry(ureg: Union[pint.UnitRegistry, pint.ApplicationRegistry]) -> None:
    """
    Set unit registry. By default, Pinttrs uses the
    `application registry <https://pint.readthedocs.io/en/stable/getting/pint-in-your-projects.html#having-a-shared-registry>`_).

    :param ureg: Unit registry.
    :raises: :class:`TypeError` if ``ureg`` is not a :class:`pint.UnitRegistry`.

    .. versionchanged:: 24.1.0
       The default registry is now the application registry.
    """
    global unit_registry
    if not isinstance(ureg, (pint.UnitRegistry, pint.ApplicationRegistry)):
        raise TypeError(
            "ureg must be a pint.UnitRegistry or pint.ApplicationRegistry instance"
        )
    unit_registry = ureg


def get_unit_registry() -> Union[pint.UnitRegistry, pint.ApplicationRegistry]:
    """
    Get default unit registry. By default, Pinttrs uses the
    `application registry <https://pint.readthedocs.io/en/stable/getting/pint-in-your-projects.html#having-a-shared-registry>`_).

    .. versionchanged:: 24.1.0
       The default registry is now the application registry.
    """
    global unit_registry
    return unit_registry
