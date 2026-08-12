from typing import Annotated

import pint
import pytest
from pydantic import BaseModel, ValidationError

import pintext
from pintext import UnitContext, UnitGenerator
from pintext.pydantic import Quantity, Units, quantity

ureg = pint.UnitRegistry()


@pytest.fixture(autouse=True)
def _use_local_registry():
    """Point the global registry at this module's registry for the test run."""
    saved = pintext.get_unit_registry()
    pintext.set_unit_registry(ureg)
    yield
    pintext.set_unit_registry(saved)


class TestPydanticUnits:
    def test_unitless_input(self):
        """Unitless values are attached the declared units."""

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units(ureg.m)]

        assert Sphere(radius=1.0).radius == 1.0 * ureg.m

    def test_quantity_input(self):
        """Quantities with compatible units pass through unchanged."""

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units(ureg.m)]

        r = 1.0 * ureg.km
        s = Sphere(radius=r)
        assert s.radius is r

    def test_convert(self):
        """``convert=True`` forces conversion to the declared units."""

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units(ureg.m, convert=True)]

        s = Sphere(radius=1.0 * ureg.km)
        assert s.radius.m == 1000.0
        assert s.radius.u == ureg.m

    def test_units_dict_input(self):
        """Mappings are interpreted with to_quantity()."""

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units(ureg.m)]

        assert Sphere(radius={"value": 2.0, "units": "km"}).radius == 2.0 * ureg.km
        assert Sphere(radius={"magnitude": 2.0, "unit": "km"}).radius == 2.0 * ureg.km
        assert Sphere(radius={"m": 100.0, "u": "cm"}).radius == 100.0 * ureg.cm

    def test_string_input(self):
        """
        Unit-carrying strings are interpreted; plain magnitudes keep default units.
        """

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units(ureg.m)]

        assert Sphere(radius="2 km").radius == 2.0 * ureg.km
        # A bare numeric string is unitless, not dimensionless
        assert Sphere(radius="2").radius == 2.0 * ureg.m
        # to_quantity() would make this dimensionless, losing the default units
        assert Sphere(radius=[1.0, 2.0]).radius.units == ureg.m

    @pytest.mark.parametrize("value", ["text", "(", "3 +", "1/0"])
    def test_reject_unparsable_string(self, value):
        """Strings Pint cannot parse are reported as a ValidationError."""

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units(ureg.m)]

        class Bare(BaseModel):
            radius: Quantity

        with pytest.raises(ValidationError):
            Sphere(radius=value)

        with pytest.raises(ValidationError):
            Bare(radius=value)

    def test_reject_incompatible_units(self):
        """Incompatible units are reported as a pydantic ValidationError."""

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units(ureg.m)]

        with pytest.raises(ValidationError):
            Sphere(radius=1.0 * ureg.s)

    def test_units_as_string(self):
        """Units may be declared as a string."""

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units("m")]

        assert Sphere(radius=1.0).radius == 1.0 * ureg.m

    def test_reject_bad_units_spec(self):
        """An unusable units specification raises at type construction time."""
        with pytest.raises(TypeError):
            Units(1.0)

    def test_deferred(self):
        """A UnitGenerator defers unit evaluation to validation time."""
        ugen = UnitGenerator(ureg.m)

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units(ugen)]

        assert Sphere(radius=1.0).radius == 1.0 * ureg.m
        with ugen.override(ureg.km):
            assert Sphere(radius=1.0).radius == 1.0 * ureg.km
        assert Sphere(radius=1.0).radius == 1.0 * ureg.m

    def test_unit_context(self):
        """Unit contexts drive validation through UnitContext.deferred()."""
        uctx = UnitContext({"length": ureg.m})

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units(uctx.deferred("length"))]

        assert Sphere(radius=1.0).radius == 1.0 * ureg.m
        with uctx.override(length="km"):
            assert Sphere(radius=1.0).radius == 1.0 * ureg.km

    def test_json_roundtrip(self):
        """Serialization round-trips through the to_quantity() mapping form."""

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units(ureg.m)]

        dumped = Sphere(radius=1.0 * ureg.km).model_dump_json()
        assert dumped == '{"radius":{"value":1.0,"units":"kilometer"}}'
        assert Sphere.model_validate_json(dumped).radius == 1.0 * ureg.km

    def test_json_roundtrip_array(self):
        """Array magnitudes serialize as JSON arrays, as the schema advertises."""
        np = pytest.importorskip("numpy")

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units(ureg.m)]

        dumped = Sphere(radius=np.array([1.0, 2.0]) * ureg.km).model_dump_json()
        assert dumped == '{"radius":{"value":[1.0,2.0],"units":"kilometer"}}'
        assert (Sphere.model_validate_json(dumped).radius == [1.0, 2.0] * ureg.km).all()

    def test_units_json_schema(self):
        """A JSON schema is produced despite the plain validator function."""

        class Sphere(BaseModel):
            radius: Annotated[pint.Quantity, Units(ureg.m)]

        schema = Sphere.model_json_schema()
        radius = schema["properties"]["radius"]
        assert radius["type"] == "object"
        assert set(radius["required"]) == {"value", "units"}

    def test_repr(self):
        """Units has a readable repr."""
        assert repr(Units(ureg.m)) == (
            "Units(UnitGenerator(units=<Unit('meter')>), convert=False)"
        )
        assert repr(Units()) == "Units(None, convert=False)"


class TestPydanticQuantity:
    def test_factory_matches_units(self):
        """quantity() is a concise equivalent of the Annotated + Units spelling."""
        annotated = quantity(ureg.m)
        assert annotated.__origin__ is pint.Quantity

        (metadata,) = annotated.__metadata__
        assert isinstance(metadata, Units)
        assert metadata.unit_generator() == ureg.m
        assert metadata.convert is False

        # And it works as a field type
        class Sphere(BaseModel):
            radius: quantity(ureg.m)  # ty: ignore[invalid-type-form]

        assert Sphere(radius=1.0).radius == 1.0 * ureg.m

    def test_factory_convert(self):
        """quantity() forwards convert=."""
        (metadata,) = quantity(ureg.m, convert=True).__metadata__
        assert metadata.convert is True

    def test_bare_quantity(self):
        """The bare Quantity type accepts any quantity and applies no default."""

        class Model(BaseModel):
            q: Quantity

        assert Model(q=1.0 * ureg.s).q == 1.0 * ureg.s
        assert Model(q={"value": 5.0, "units": "s"}).q == 5.0 * ureg.s

        # Unitless values cannot be interpreted
        with pytest.raises(ValidationError):
            Model(q=1.0)
