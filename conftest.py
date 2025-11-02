"""Test configuration for pytest."""

import pytest


@pytest.fixture(autouse=True)
def add_doctest_imports(doctest_namespace):
    """Add common imports to doctest namespace.

    This allows doctests in docstrings to use these imports without
    explicitly importing them, keeping examples clean and readable.
    """
    import attrs
    import numpy
    import pint
    import xarray

    import pinttrs
    from pinttrs import field
    from pinttrs.converters import ensure_units, to_quantity
    from pinttrs.validators import has_compatible_units

    # Add to namespace
    doctest_namespace["attrs"] = attrs
    doctest_namespace["pint"] = pint
    doctest_namespace["ureg"] = pinttrs.get_unit_registry()
    doctest_namespace["pinttrs"] = pinttrs
    doctest_namespace["field"] = field
    doctest_namespace["ensure_units"] = ensure_units
    doctest_namespace["to_quantity"] = to_quantity
    doctest_namespace["has_compatible_units"] = has_compatible_units
    doctest_namespace["np"] = numpy
    doctest_namespace["xr"] = xarray
