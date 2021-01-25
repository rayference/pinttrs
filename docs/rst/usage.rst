Usage
=====

Attaching units to attributes
-----------------------------

Pinttrs's main functionality is to provide support natural unit support to
``attrs`` classes. Units must be specified explicitly, *i.e.* they cannot be
specified using a string representation, because Pinttrs does not provide a
Pint unit registry. Therefore, the first thing you need to do is to create a
Pint unit registry:

.. doctest::

   >>> import pint
   >>> ureg = pint.UnitRegistry()

Pinttrs defines a :func:`pinttr.ib` function similar to :func:`attr.ib`, which
basically calls the latter after defining some metadata. The ``units`` argument
is the main difference and allows for the attachment of units to a field:

.. doctest::

   >>> import attr, pinttr
   >>> @attr.s
   ... class MyClass:
   ...     field = pinttr.ib(units=ureg.km)
   >>> MyClass(1.0)
   MyClass(field=<Quantity(1.0, 'kilometer')>)

Scalar values are automatically wrapped in Pint units. If a Pint quantity is
passed as an attribute value, its units will be checked. If they prove to be
compatible in the sense of Pinttrs, the value will be assigned to the attribute
without modification:

.. doctest::

   >>> MyClass(1.0 * ureg.m)
   MyClass(field=<Quantity(1.0, 'meter')>)

If units are incompatible, the built-in validator will fail and raise a
:class:`~pinttr.exceptions.UnitsError`:

.. doctest::

   >>> MyClass(1.0 * ureg.s)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "<attrs generated init __main__.MyClass>", line 5, in __init__
     File "/home/m4urice/Documents/src/pinttrs/src/pinttr/validators.py", line 14, in has_compatible_units
       raise UnitsError(
   pinttr.exceptions.UnitsError: Cannot convert from 'second' to 'kilometer': incompatible units 'second' used to set field 'field' (allowed: 'kilometer').

By default, the created attribute also applies conversion and validation upon
setting:

.. doctest::

   >>> o = MyClass(1.0)
   >>> o
   MyClass(field=<Quantity(1.0, 'kilometer')>)
   >>> o.field = 1.0 * ureg.s
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "<attrs generated init __main__.MyClass>", line 5, in __init__
     File "/home/m4urice/Documents/src/pinttrs/src/pinttr/validators.py", line 14, in has_compatible_units
       raise UnitsError(
   pinttr.exceptions.UnitsError: Cannot convert from 'second' to 'kilometer': incompatible units 'second' used to set field 'field' (allowed: 'kilometer').
   >>> o.field = 1.0 * ureg.m
   >>> o
   MyClass(field=<Quantity(1.0, 'meter')>)
   >>> o.field = 1.0
   >>> o
   MyClass(field=<Quantity(1.0, 'kilometer')>)

Using callables to dynamically change default units
---------------------------------------------------

The :func:`pinttr.ib` function's ``units`` parameter also accepts callables. 
When this happens, the store callable is evaluate each time units are requested,
*e.g.* by a converter or a validator:

.. doctest::

   >>> @attr.s
   ... class MyClass:
   ...     field = pinttr.ib(units=lambda: ureg.m)
   >>> MyClass(1.0)
   MyClass(field=<Quantity(1.0, 'meter')>)

Callables can be used to vary default units dynamically at runtime:

.. doctest::

   >>> default_units = ureg.m
   >>> @attr.s
   ... class MyClass:
   ...     field = pinttr.ib(units=lambda: default_units)
   >>> MyClass(1.0)
   MyClass(field=<Quantity(1.0, 'meter')>)
   >>> default_units = ureg.s
   >>> MyClass(1.0)
   MyClass(field=<Quantity(1.0, 'second')>)

Default units with contextual overrides
---------------------------------------

Coming soon.

Dict-based object initialisation with units
-------------------------------------------

Pinttrs ships a helper function :func:`pinttr.util.interpret_units` which can be 
used to interpret units in a dictionary with string-valued keys:

.. doctest::

   >>> pinttr.util.interpret_units({"field": 1.0, "field_units": "m"}, ureg)
   {'field': <Quantity(1.0, 'meter')>}

This is useful to *e.g.* initialise objects using simple JSON fragments. 
Example:

.. doctest::

   >>> from pinttr.util import interpret_units
   >>> MyClass(**interpret_units({"field": 1.0, "field_units": "s"}, ureg))
   MyClass(field=<Quantity(1.0, 'second')>)
   >>> MyClass(**interpret_units({"field": 1.0, "field_units": "m"}, ureg))
   Traceback (most recent call last):
     File "/Users/m4urice/miniconda3/envs/pinttrs/lib/python3.6/doctest.py", line 1330, in __run
       compileflags, 1), test.globs)
     File "<doctest default[2]>", line 1, in <module>
       MyClass(**interpret_units({"field": 1.0, "field_units": "m"}, ureg))
     File "<attrs generated init builtins.MyClass-3>", line 5, in __init__
       __attr_validator_field(self, __attr_field, self.field)
     File "/Users/m4urice/Documents/src/perso/pinttrs/src/pinttr/validators.py", line 20, in has_compatible_units
       extra_msg=f": incompatible units '{value.units}' "
   pinttr.exceptions.UnitsError: Cannot convert from 'meter' to 'second': incompatible units 'meter' used to set field 'field' (allowed: 'second').

.. note::

   The same unit registry must be used to define field units and interpret 
   dictionaries.