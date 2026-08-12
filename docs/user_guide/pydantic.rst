.. _usage-pydantic:

pydantic integration
====================

This extension requires that the pydantic (v2) package is installed.
If not done externally in your project, it can be requested with the ``pydantic``
extra:

.. code-block:: bash

   python -m pip install "pintext[pydantic]"

Pintext exposes three names for pydantic:
:class:`~pintext.pydantic.Units`, the annotation attaching units to a field;
:data:`~pintext.pydantic.Quantity`, which accepts any quantity; and
:func:`~pintext.pydantic.quantity`, a concise shorthand.

Declaring units
---------------

:class:`~pintext.pydantic.Units` is used as :data:`~typing.Annotated`
metadata:

.. doctest::

    >>> from typing import Annotated
    >>> import pint, pintext
    >>> from pydantic import BaseModel, ValidationError
    >>> from pintext.pydantic import Units
    >>> ureg = pintext.get_unit_registry()
    >>> class Sphere(BaseModel):
    ...     radius: Annotated[pint.Quantity, Units(ureg.m)]
    >>> Sphere(radius=1.0).radius
    <Quantity(1.0, 'meter')>

:func:`~pintext.pydantic.quantity` is a shorthand for the same thing:

.. doctest::

    >>> from pintext.pydantic import quantity
    >>> class Sphere(BaseModel):
    ...     radius: quantity(ureg.m)
    >>> Sphere(radius=1.0).radius
    <Quantity(1.0, 'meter')>

.. warning::
    ``quantity(...)`` is a *function call*, which static type checkers reject
    inside an annotation — the same reason pydantic deprecated ``conint`` and
    ``constr``. Use the :class:`~pintext.pydantic.Units` spelling wherever
    static checking matters; ``quantity()`` is a convenience for interactive
    use.

Units may also be given as a string, interpreted against the registry returned
by :func:`.get_unit_registry`:

.. doctest::

    >>> class Sphere(BaseModel):
    ...     radius: Annotated[pint.Quantity, Units("m")]
    >>> Sphere(radius=1.0).radius
    <Quantity(1.0, 'meter')>

Quantities with compatible units pass through unchanged; ``convert=True``
forces conversion to the declared units:

.. doctest::

    >>> Sphere(radius=1.0 * ureg.km).radius
    <Quantity(1.0, 'kilometer')>
    >>> class ConvertingSphere(BaseModel):
    ...     radius: Annotated[pint.Quantity, Units(ureg.m, convert=True)]
    >>> ConvertingSphere(radius=1.0 * ureg.km).radius
    <Quantity(1000.0, 'meter')>

Incompatible units are reported as a regular :class:`~pydantic.ValidationError`,
so they compose with pydantic's error collection:

.. doctest::

    >>> try:
    ...     Sphere(radius=1.0 * ureg.s)
    ... except ValidationError as e:
    ...     print(type(e).__name__)
    ValidationError

.. note::
    :class:`~pintext.exceptions.UnitsError` derives from :class:`TypeError`,
    which pydantic does not collect into a
    :class:`~pydantic.ValidationError`. The integration therefore re-raises it
    as a :class:`ValueError`, keeping the original exception as the
    ``__cause__``.

Dictionary input
----------------

Serialized values — mappings, unit-carrying strings and
:class:`xarray.DataArray` objects — are passed through :func:`.to_quantity`
first, which is what makes loading from JSON or YAML work:

.. doctest::

   >>> Sphere(radius={"value": 2.0, "units": "km"}).radius
   <Quantity(2.0, 'kilometer')>
   >>> Sphere(radius="2 km").radius
   <Quantity(2, 'kilometer')>

Plain magnitudes are not: they receive the field's default units instead of
being made dimensionless.

Serialization produces the same form, so models round-trip:

.. doctest::

    >>> dumped = Sphere(radius=1.0 * ureg.km).model_dump_json()
    >>> dumped
    '{"radius":{"value":1.0,"units":"kilometer"}}'
    >>> Sphere.model_validate_json(dumped).radius
    <Quantity(1.0, 'kilometer')>

A JSON schema is produced as well:

.. doctest::

    >>> Sphere.model_json_schema()["properties"]["radius"]["required"]
    ['value', 'units']

Unit contexts
-------------

The ``units`` argument accepts a :class:`.UnitGenerator`, which defers
evaluation to validation time. Combined with
:meth:`.UnitContext.deferred`, this makes a whole model tree read its unitless
inputs according to the active context:

.. doctest::

    >>> uctx = pintext.UnitContext({"length": ureg.m})
    >>> class Sphere(BaseModel):
    ...     radius: Annotated[pint.Quantity, Units(uctx.deferred("length"))]
    >>> Sphere(radius=1.0).radius
    <Quantity(1.0, 'meter')>
    >>> with uctx.override(length="km"):
    ...     Sphere(radius=1.0).radius
    <Quantity(1.0, 'kilometer')>

Accepting any quantity
----------------------

When a field should hold a quantity but has no declared units, use
:data:`~pintext.pydantic.Quantity`. No default units are applied and no
compatibility check is performed, but mappings are still interpreted:

.. doctest::

    >>> from pintext.pydantic import Quantity
    >>> class Measurement(BaseModel):
    ...     value: Quantity
    >>> Measurement(value={"value": 5.0, "units": "s"}).value
    <Quantity(5.0, 'second')>

A value that cannot be interpreted as a quantity is rejected:

.. doctest::

    >>> try:
    ...     Measurement(value=1.0)
    ... except ValidationError as e:
    ...     print(type(e).__name__)
    ValidationError

.. note::
    Because the annotation supplies its own core schema, models holding
    quantities need no ``arbitrary_types_allowed`` configuration.
