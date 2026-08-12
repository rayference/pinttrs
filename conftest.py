"""Test configuration for pytest."""

import pytest


@pytest.fixture(autouse=True)
def add_doctest_imports(doctest_namespace):
    """Add common imports to doctest namespace.

    This allows doctests in docstrings to use these imports without
    explicitly importing them, keeping examples clean and readable.

    Optional dependencies are guarded so that core doctests still run on a
    minimal (pint-only) install.
    """
    import pint

    import pintext
    from pintext import (
        UnitContext,
        UnitGenerator,
        check_units,
        ensure_units,
        to_quantity,
        units_compatible,
    )

    # Core namespace
    doctest_namespace["pint"] = pint
    doctest_namespace["pintext"] = pintext
    doctest_namespace["ureg"] = pintext.get_unit_registry()
    doctest_namespace["UnitContext"] = UnitContext
    doctest_namespace["UnitGenerator"] = UnitGenerator
    doctest_namespace["check_units"] = check_units
    doctest_namespace["ensure_units"] = ensure_units
    doctest_namespace["to_quantity"] = to_quantity
    doctest_namespace["units_compatible"] = units_compatible

    # Optional dependencies
    try:
        import attrs

        from pintext.attrs import field, has_compatible_units

        doctest_namespace["attrs"] = attrs
        doctest_namespace["field"] = field
        doctest_namespace["has_compatible_units"] = has_compatible_units
    except ImportError:
        pass

    try:
        import pydantic

        from pintext.pydantic import Quantity, quantity

        doctest_namespace["pydantic"] = pydantic
        doctest_namespace["Quantity"] = Quantity
        doctest_namespace["quantity"] = quantity
    except ImportError:
        pass

    try:
        import numpy

        doctest_namespace["np"] = numpy
    except ImportError:
        pass

    try:
        import xarray

        doctest_namespace["xr"] = xarray
    except ImportError:
        pass
