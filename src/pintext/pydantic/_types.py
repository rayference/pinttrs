from collections.abc import Mapping
from typing import Annotated, Any

import pint
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from .._generator import UnitGenerator
from .._registry import get_unit_registry
from ..converters import _PINT_PARSE_ERRORS, ensure_units, to_quantity
from ..exceptions import UnitsError
from ..util import check_units


def _as_unit_generator(units: pint.Unit | UnitGenerator | str) -> UnitGenerator:
    """
    Normalize a unit specification to a :class:`~pintext.UnitGenerator`.

    Strings are interpreted using the registry returned by
    :func:`~pintext.get_unit_registry`.
    """
    if isinstance(units, UnitGenerator):
        return units
    if isinstance(units, str):
        return UnitGenerator(get_unit_registry().Unit(units))
    if isinstance(units, pint.Unit):
        return UnitGenerator(units)
    raise TypeError(
        "Argument 'units' must be a str, a pint.Unit or a UnitGenerator; "
        f"got {type(units)}"
    )


def _is_serialized(value: Any) -> bool:
    """
    Check whether a value carries its own units and must therefore be passed to
    :func:`~pintext.to_quantity` before default units are applied.

    .. note::
        Strings are deliberately left aside: they may, or not, carry unit
        information, and thus require different processing.
    """
    if isinstance(value, Mapping):
        return True

    try:
        import xarray as xr
    except ImportError:
        return False

    return isinstance(value, xr.DataArray)


class Units:
    """
    Pydantic annotation turning a field into a Pint quantity.

    Use it as :data:`~typing.Annotated` metadata::

        radius: Annotated[pint.Quantity, Units(ureg.m)]

    This is the spelling static type checkers understand. :func:`quantity` is a
    more concise equivalent, at the cost of being a function call in an
    annotation, which type checkers reject.

    :param units:
        Units attached to the field. A :class:`~pintext.UnitGenerator` (*e.g.*
        obtained from :meth:`.UnitContext.deferred()`) defers unit evaluation to
        validation time, which makes unit contexts apply. Strings are
        interpreted using the registry returned by
        :func:`~pintext.get_unit_registry`. If ``None``, any quantity is
        accepted, no default units are applied and no compatibility check is
        performed.

    :param convert:
        If ``True``, quantities are converted to ``units`` instead of being
        passed through unchanged.
    """

    __slots__ = ("convert", "unit_generator")

    def __init__(
        self,
        units: pint.Unit | UnitGenerator | str | None = None,
        *,
        convert: bool = False,
    ):
        self.unit_generator = None if units is None else _as_unit_generator(units)
        self.convert = convert

    def __repr__(self) -> str:
        return f"Units({self.unit_generator!r}, convert={self.convert!r})"

    def _validate(self, value: Any) -> pint.Quantity:
        # Interpret serialized input, which carry unit information.
        # Plain magnitudes are left untouched: to_quantity() would make them
        # dimensionless and default units would never apply.
        if _is_serialized(value):
            value = to_quantity(value)

        # Without default units, value must resolve to a quantity on its own
        if self.unit_generator is None:
            if isinstance(value, str):
                value = to_quantity(
                    value, strict=True
                )  # raises ValueError upon parse failure

            if not isinstance(value, pint.Quantity):
                raise ValueError(f"Cannot interpret {value!r} as a Pint quantity")

            return value

        # Deferred evaluation: honours UnitContext.override()
        units = self.unit_generator()

        # Pydantic collects neither the exceptions Pint raises on a string it
        # cannot parse, nor UnitsError (which derives from TypeError): re-raise
        # both as ValueError
        try:
            value = ensure_units(value, default_units=units, convert=self.convert)
            check_units(value, units)
        except _PINT_PARSE_ERRORS as e:
            raise ValueError(f"Cannot interpret {value!r} as a Pint quantity") from e
        except UnitsError as e:
            raise ValueError(str(e)) from e

        return value

    @staticmethod
    def _serialize(value: pint.Quantity) -> dict:
        magnitude = value.magnitude
        # Array magnitudes are not JSON-serializable as such
        if hasattr(magnitude, "tolist"):
            magnitude = magnitude.tolist()
        return {"value": magnitude, "units": str(value.units)}

    def __get_pydantic_core_schema__(
        self, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            self._validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                self._serialize, when_used="json"
            ),
        )

    def __get_pydantic_json_schema__(
        self, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "object",
            "properties": {
                "value": {
                    "anyOf": [{"type": "number"}, {"type": "array"}],
                    "title": "Value",
                },
                "units": {"type": "string", "title": "Units"},
            },
            "required": ["value", "units"],
        }


# Docstring for this alias lives in __init__.py (not rendered by Sphinx otherwise)
Quantity = Annotated[pint.Quantity, Units()]


def quantity(units: pint.Unit | UnitGenerator | str, *, convert: bool = False) -> Any:
    """
    Build an annotated type for a field holding a Pint quantity with declared
    units.

    Values are interpreted as follows:

    * mappings and xarray DataArrays are first passed to
      :func:`~pintext.to_quantity`;
    * strings are parsed by :func:`~pintext.ensure_units`, which means that
      those carrying no units are attached ``units``;
    * unitless values are attached ``units``;
    * quantities are checked for unit compatibility with
      :func:`~pintext.check_units`.

    :param units:
        Units attached to the field. A :class:`~pintext.UnitGenerator` (*e.g.*
        obtained from :meth:`.UnitContext.deferred`)
        defers unit evaluation to validation time, which makes unit contexts
        effective. Strings are interpreted using the registry returned by
        :func:`~pintext.get_unit_registry`.

    :param convert:
        If ``True``, quantities are converted to ``units`` instead of being
        passed through unchanged.

    :returns:
        An :data:`~typing.Annotated` alias usable as a pydantic field type.

    .. note::
       Because this is a function call, static type checkers reject it inside
       an annotation. Use the equivalent :class:`Units` spelling
       (``Annotated[pint.Quantity, Units(ureg.m)]``) where static checking
       matters.

    .. rubric:: Examples

    >>> from pydantic import BaseModel
    >>> class Sphere(BaseModel):
    ...     radius: quantity(ureg.m)
    >>> Sphere(radius=1.0).radius
    <Quantity(1.0, 'meter')>
    >>> Sphere(radius={"value": 2.0, "units": "km"}).radius
    <Quantity(2.0, 'kilometer')>

    Incompatible units are rejected:

    >>> Sphere(radius=1.0 * ureg.s)
    Traceback (most recent call last):
      ...
    pydantic_core._pydantic_core.ValidationError: ...

    Units declared through a unit context are evaluated at validation time:

    >>> uctx = UnitContext({"length": ureg.m})
    >>> class Sphere(BaseModel):
    ...     radius: quantity(uctx.deferred("length"))
    >>> with uctx.override(length="km"):
    ...     Sphere(radius=1.0).radius
    <Quantity(1.0, 'kilometer')>

    Serialization round-trips through the mapping form read by
    :func:`~pintext.converters.to_quantity`:

    >>> Sphere(radius=1.0).model_dump_json()
    '{"radius":{"value":1.0,"units":"meter"}}'
    """
    return Annotated[pint.Quantity, Units(units, convert=convert)]
