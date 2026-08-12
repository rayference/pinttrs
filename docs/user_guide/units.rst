.. _usage-units:

Units, converters and compatibility
===================================

This page covers the supporting machinery around :doc:`unit_contexts`: where
units come from, how they are attached to values, and what Pintext considers
"compatible".

The unit registry
-----------------

Pint requires units to be created by a unit registry. Pintext keeps a module
-level default, which is Pint's
`application registry <https://pint.readthedocs.io/en/stable/getting/pint-in-your-projects.html#having-a-shared-registry>`_
unless changed with :func:`.set_unit_registry`:

.. doctest::

   >>> import pintext
   >>> ureg = pintext.get_unit_registry()
   >>> ureg.m
   <Unit('meter')>

.. note::

   Pintext deliberately does not interpret unit strings automatically
   everywhere. Doing so against the built-in registry is a source of trouble
   for users who also manipulate units created with a different registry —
   quantities from two registries cannot be combined. The places that *do*
   accept strings say so explicitly.

.. _usage-units-ensure_units:

Attaching units
---------------

:func:`.ensure_units` wraps a value in a Pint quantity. It works in two modes.

**Immediate mode** converts a value directly:

.. doctest::

   >>> pintext.ensure_units(100.0, default_units=ureg.m)
   <Quantity(100.0, 'meter')>

Values that already carry units pass through unchanged:

.. doctest::

   >>> pintext.ensure_units(100.0 * ureg.km, default_units=ureg.m)
   <Quantity(100.0, 'kilometer')>

Set ``convert=True`` to force conversion:

.. doctest::

   >>> pintext.ensure_units(100.0 * ureg.km, default_units=ureg.m, convert=True)
   <Quantity(100000.0, 'meter')>

**Deferred mode** — omitting the value — returns a converter function. This is
the form used by the class-framework integrations, and the form that makes unit
contexts effective, since ``default_units`` is re-evaluated on every call:

.. doctest::

   >>> generator = pintext.UnitGenerator(ureg.m)
   >>> converter = pintext.ensure_units(default_units=generator)
   >>> converter(1.0)
   <Quantity(1.0, 'meter')>
   >>> with generator.override(ureg.km):
   ...     converter(1.0)
   <Quantity(1.0, 'kilometer')>

.. _usage-units-to_quantity:

Interpreting serialized quantities
----------------------------------

:func:`.to_quantity` turns serialized representations of a quantity into a Pint
quantity. Values Pint cannot interpret pass through unchanged, which makes it
safe to apply indiscriminately.

Mappings carry the magnitude under ``value``, ``magnitude`` or ``m``, and the
units under ``units``, ``unit`` or ``u``:

.. doctest::

   >>> pintext.to_quantity({"value": 1.0, "units": "m"})
   <Quantity(1.0, 'meter')>
   >>> pintext.to_quantity({"magnitude": 2.5, "unit": "km"})
   <Quantity(2.5, 'kilometer')>
   >>> pintext.to_quantity({"m": 100.0, "u": "cm"})
   <Quantity(100.0, 'centimeter')>

This is the pattern to use when loading from JSON or YAML. Extra keys are
rejected rather than ignored, so typos surface immediately:

.. doctest::

   >>> pintext.to_quantity({"value": 1.0, "units": "m", "unts": "km"})
   Traceback (most recent call last):
       ...
   ValueError: Supplied value has extra unused keys ['unts']

:class:`xarray.DataArray` objects following CF conventions are also supported,
reading units from the ``units`` attribute:

.. doctest::

   >>> import xarray as xr
   >>> pintext.to_quantity(xr.DataArray([1.0, 2.0, 3.0], attrs={"units": "m"}))
   <Quantity([1. 2. 3.], 'meter')>

Anything else is handed to Pint: unit-carrying strings are parsed, and unitless
values become dimensionless quantities.

.. doctest::

   >>> pintext.to_quantity("2 m")
   <Quantity(2, 'meter')>
   >>> pintext.to_quantity(42.0)
   <Quantity(42.0, 'dimensionless')>

Values Pint cannot interpret are returned as-is. Pass ``strict=True`` to raise
instead:

.. doctest::

   >>> pintext.to_quantity("text")
   'text'
   >>> pintext.to_quantity("text", strict=True)
   Traceback (most recent call last):
       ...
   ValueError: Conversion of value to quantity failed (got 'text')

.. warning::
   :func:`.to_quantity` uses the registry returned by
   :func:`.get_unit_registry`, not any registry attached to a unit context.

.. _compatible:

What are "compatible units"?
----------------------------

Pintext's notion of compatible units extends beyond dimensionality. In many
contexts, adding presumably dimensionless quantities together is not
meaningful.

The need emerged when manipulating angles. Pint behaves well when converting
them:

.. doctest::

   >>> from math import pi
   >>> pi * ureg.rad + 180 * ureg.deg
   <Quantity(6.28318531, 'radian')>

However, operations involving unitless values can be unintuitive. While this is
natural:

.. doctest::

   >>> 1 + 1 * ureg.rad
   <Quantity(2, 'dimensionless')>

this is harder to anticipate:

.. doctest::

   >>> 1 + 1 * ureg.deg
   <Quantity(1.01745329, 'dimensionless')>

and mixing angles with solid angles is stranger still:

.. doctest::

   >>> 1 * ureg.deg + 1 * ureg.sr
   <Quantity(58.2957795, 'degree')>

Pint does not treat angle units as a special case and offers no facility to
prevent conversion from, say, degree to steradian. It will likewise not declare
radiance (W/m²/sr) and irradiance (W/m²) incompatible.

For this reason Pintext implements a stricter check,
:func:`.units_compatible`, which declares dimensionless quantities with
inconvertible units incompatible. Where Pint reports compatibility:

.. doctest::

   >>> u1 = ureg.Unit("W/m^2/sr")
   >>> u2 = ureg.Unit("W/m^2")
   >>> u1.is_compatible_with(u2)
   True

Pintext does not:

.. doctest::

   >>> pintext.units_compatible(u1, u2)
   False

This does not prevent adding radiances to irradiances, but it does provide a
means to check that an attribute expecting a radiance is not handed an
irradiance.

Checking a value
^^^^^^^^^^^^^^^^

:func:`.check_units` applies that comparison to a value and raises
:class:`.UnitsError` on failure. It is the shared check behind both the *attrs*
and *pydantic* integrations:

.. doctest::

   >>> pintext.check_units(1.0 * ureg.km, ureg.m)
   >>> pintext.check_units(1.0 * ureg.s, ureg.m)
   Traceback (most recent call last):
       ...
   pintext.exceptions.UnitsError: Cannot convert from 'second' to 'meter': incompatible units 'second' used to set value (allowed: 'meter').

Unitless values are rejected too — a quantity is required:

.. doctest::

   >>> pintext.check_units(1.0, ureg.m)
   Traceback (most recent call last):
       ...
   pintext.exceptions.UnitsError: Cannot convert from 'None' to 'meter': unitless value '1.0' used to set value (requires units 'meter').

Passing ``name`` reports the offending field:

.. doctest::

   >>> pintext.check_units(1.0 * ureg.s, ureg.m, name="radius")
   Traceback (most recent call last):
       ...
   pintext.exceptions.UnitsError: Cannot convert from 'second' to 'meter': incompatible units 'second' used to set field 'radius' (allowed: 'meter').
