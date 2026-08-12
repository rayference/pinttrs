"""
*pydantic* integration.

Requires the ``pydantic`` extra::

    pip install "pintext[pydantic]"
"""

try:
    import pydantic as _pydantic  # noqa: F401
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "pintext.pydantic requires the 'pydantic' extra: "
        "pip install 'pintext[pydantic]'"
    ) from e

from ._types import Quantity as _Quantity
from ._types import Units, quantity

#: Any Pint quantity. Mappings and xarray DataArrays are interpreted with
#: :func:`~pintext.to_quantity`; no default units are applied and no
#: compatibility check is performed. A value that cannot be interpreted as a
#: quantity (*e.g.* bare :class:`float`) is rejected.
#:
#: Use :class:`Units` or :func:`quantity` instead when the field has declared
#: units.
#:
#: .. seealso:: :ref:`usage-pydantic`
Quantity = _Quantity

__all__ = ["Quantity", "Units", "quantity"]
