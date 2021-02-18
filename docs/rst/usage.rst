.. _usage:

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

.. note:: If ``units`` is unset, :func:`pinttr.ib` behaves exactly like
   :func:`attr.ib`.

Scalar values are automatically wrapped in Pint units. If a Pint quantity is
passed as an attribute value, its units will be checked. If they prove to be
:ref:`compatible in the sense of Pinttrs <compatible>`, the value will be
assigned to the attribute without modification:

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

Unit generators
---------------

Pinttrs provides facilities to dynamically vary default units applied when
passing a unitless value to a field to which units are attached. The central
component of this workflow is the :class:`.UnitGenerator` class. This small
class stores Pint units and returns them when called:

.. doctest::

   >>> ugen = pinttr.UnitGenerator(ureg.m)
   >>> ugen()
   <Unit('meter')>

Stored units can then be dynamically modified:

.. doctest::

   >>> ugen.units = ureg.s
   >>> ugen()
   <Unit('second')>

The :func:`pinttr.ib` function's ``units`` parameter also accepts unit
generators. When this happens, the stored generator is evaluated each time units
are requested, *e.g.* by a converter or a validator:

.. doctest::

   >>> ugen = pinttr.UnitGenerator(ureg.m)
   >>> @attr.s
   ... class MyClass:
   ...     field = pinttr.ib(units=ugen)
   >>> MyClass(1.0)
   MyClass(field=<Quantity(1.0, 'meter')>)

.. note:: Under the hood, units attached to attributes with :func:`pinttr.ib`
   are always stored as unit generators.

Temporary override
^^^^^^^^^^^^^^^^^^

The :meth:`.UnitGenerator.override` context manager can also be used to modify
stored units temporarily:

.. doctest::

   >>> ugen.units = ureg.m
   >>> with ugen.override(ureg.s):
   ...     ugen()
   <Unit('second')>
   >>> ugen()
   <Unit('meter')>

Override values can be specified using strings, which are interpreted based on
the registry associated to the currently stored units:

.. doctest::

   >>> with ugen.override("m"):
   ...     ugen()
   <Unit('meter')>

Override can be used to vary dynamically default units attached to an attribute:

.. doctest::

   >>> ugen = pinttr.UnitGenerator(ureg.m)
   >>> @attr.s
   ... class MyClass:
   ...     field = pinttr.ib(units=ugen)
   >>> MyClass(1.0)
   MyClass(field=<Quantity(1.0, 'meter')>)
   >>> with ugen.override(ureg.s):
   ...     MyClass(1.0)
   MyClass(field=<Quantity(1.0, 'second')>)

Composed unit generators
^^^^^^^^^^^^^^^^^^^^^^^^

Unit generators can be composed to construct composed dynamic units. To that
end, the :class:`.UnitGenerator` constructor accepts a callable, which can be
a regular function, a callable class or even a lambda (even another generator
can be used, but this is of limited utility). For instance:

.. doctest::

   >>> ugen_length = pinttr.UnitGenerator(ureg.m)
   >>> ugen_time = pinttr.UnitGenerator(ureg.s)
   >>> ugen_speed = pinttr.UnitGenerator(lambda: ugen_length() / ugen_time())
   >>> ugen_speed()
   <Unit('meter / second')>

Overrides will then propagate to the composed generator:

.. doctest::

   >>> with ugen_length.override("km"), ugen_time.override("hour"):
   ...     ugen_speed()
   <Unit('kilometer / hour')>

Unit contexts
-------------

Unit contexts, implemented by the :class:`.UnitContext` class, provide a
simple interface to manage a structured collection of unit generators. Their
primary application is to vary the interpretation of units applied to scalar
values assigned to unit-attached fields.

Let's first define a unit context. :class:`.UnitContext` encapsulates a
dictionary of :class:`.UnitGenerator` values. The simplest definition uses
string-keyed dictionaries:

.. doctest::

   >>> uctx = pinttr.UnitContext({"length": pinttr.UnitGenerator(ureg.m)})

Additional units can be registered after context object creation using the
:meth:`~.UnitContext.register` method:

.. doctest::

   >>> uctx.register("time", pinttr.UnitGenerator(ureg.s))
   >>> uctx.get_all()
   {'length': <Unit('meter')>, 'time': <Unit('second')>}

The unit context can be queried for units using the :meth:`~.UnitContext.get`
method:

.. doctest::

   >>> uctx.get("length")
   <Unit('meter')>

It is also possible to access the underlying generator with the
:meth:`~.UnitContext.deferred` method:

.. doctest::

   >>> uctx.deferred("length")
   UnitGenerator(units=<Unit('meter')>)

The returned unit generator can be used to attach units to an attribute:

.. doctest::

   >>> @attr.s
   ... class MyClass:
   ...     field = pinttr.ib(units=uctx.deferred("length"))
   >>> MyClass(1.0)
   MyClass(field=<Quantity(1.0, 'meter')>)

When initialising a context or registering additional units to it, units can be
directly passed and will be turned into generators automatically:

.. doctest::

   >>> uctx = pinttr.UnitContext({"length": ureg.m})
   >>> uctx.deferred("length")
   UnitGenerator(units=<Unit('meter')>)
   >>> uctx.register("time", ureg.s)
   >>> uctx.deferred("time")
   UnitGenerator(units=<Unit('second')>)

Temporary override
^^^^^^^^^^^^^^^^^^

The :meth:`~.UnitContext.override` context manager provides a convenient way to
override one or several of the registered units with a dictionary:

.. doctest::

   >>> with uctx.override({"length": ureg.mile, "time": ureg.hour}):
   ...     ureg.Quantity(1.0, "km/hour").to(uctx.get("length") / uctx.get("time"))
   <Quantity(0.621371192, 'mile / hour')>

The :meth:`~.UnitContext.override` method also offers a keyword argument
interface, usable when keys are strings or when a key converter handling strings
is defined (see `Non-string context keys`_):

.. doctest::

   >>> with uctx.override(length=ureg.mile, time=ureg.hour):
   ...     ureg.Quantity(1.0, "km/hour").to(uctx.get("length") / uctx.get("time"))
   <Quantity(0.621371192, 'mile / hour')>

Just like :class:`.UnitGenerator`, :class:`.UnitContext` can be overridden using
string-based unit specifications:

.. doctest::

   >>> with uctx.override(length="mile", time="hour"):
   ...     ureg.Quantity(1.0, "km/hour").to(uctx.get("length") / uctx.get("time"))
   <Quantity(0.621371192, 'mile / hour')>

Non-string context keys
^^^^^^^^^^^^^^^^^^^^^^^

Sometimes, it is desirable to not use strings as context registry keys. A
typical replacement can be an enumeration, *e.g.* with string values:

.. doctest::

   >>> import enum
   >>> class PhysicalQuantity(enum.Enum):
   ...     LENGTH = "length"
   ...     SPEED = "speed"
   ...     TIME = "time"

Using a string-valued enumeration is of particular interest, because the enum's
constructor will act like a converter:

.. doctest::

   >>> PhysicalQuantity(PhysicalQuantity.LENGTH)
   <PhysicalQuantity.LENGTH: 'length'>
   >>> PhysicalQuantity("length")
   <PhysicalQuantity.LENGTH: 'length'>

In order to preserve optimal convenience, :class:`.UnitContext` offers the
possibility to declare a key converter. In our example, we would like to still
be able to access units and generators using strings (this would also make the
keyword argument of :meth:`~.UnitContext.override` still usable). Our
enumeration's constructor performs this string-to-enum conversion, so we can
declare it as the key converter:

.. doctest::

   >>> uctx = pinttr.UnitContext(key_converter=PhysicalQuantity)

We can then use strings or enum members indifferently to access context
contents:

   >>> uctx.register(PhysicalQuantity.LENGTH, ureg.m)
   >>> uctx.register("time", ureg.s)
   >>> uctx.deferred(PhysicalQuantity.TIME)
   UnitGenerator(units=<Unit('second')>)
   >>> uctx.register(PhysicalQuantity.SPEED, pinttr.UnitGenerator(
   ...     lambda: uctx.get(PhysicalQuantity.LENGTH) /
   ...             uctx.get(PhysicalQuantity.TIME)
   ... ))
   >>> with uctx.override(length=ureg.km, time=ureg.hour):
   ...    uctx.get("speed")
   <Unit('kilometer / hour')>

Specifying units with strings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`.UnitContext` can interpret string values to Pint units and construct
generators from them. The unit registry returned by :func:`.get_unit_registry`
will be used for interpretation. Example:

.. doctest::

   >>> uctx = pinttr.UnitContext({"length": "m", "time": "s"}, interpret_str=True)
   >>> uctx.get_all()
   {'length': <Unit('meter')>, 'time': <Unit('second')>}

.. warning:: Interpreting units base on Pinttrs's default registry can have
   unintended consequences. Be careful when using this feature!

   .. doctest::

      >>> uctx.get("length") / ureg.m
      Traceback (most recent call last):
          ...
      ValueError: Cannot operate with Unit and Unit of different registries.

Interpreting units in dicts
---------------------------

Pinttrs ships a helper function :func:`pinttr.interpret_units` which can be 
used to interpret units in a dictionary with string-valued keys:

.. doctest::

   >>> pinttr.interpret_units({"field": 1.0, "field_units": "m"}, ureg)
   {'field': <Quantity(1.0, 'meter')>}

This is useful to *e.g.* initialise objects using simple JSON fragments. 
Example:

.. doctest::

   >>> from pinttr import interpret_units
   >>> ugen = pinttr.UnitGenerator(ureg.m)
   >>> @attr.s
   ... class MyClass:
   ...     field = pinttr.ib(units=ugen)
   >>> MyClass(**interpret_units({"field": 1.0, "field_units": "m"}, ureg))
   MyClass(field=<Quantity(1.0, 'meter')>)
   >>> MyClass(**interpret_units({"field": 1.0, "field_units": "s"}, ureg))
   Traceback (most recent call last):
       ...
   pinttr.exceptions.UnitsError: Cannot convert from 'second' to 'meter': incompatible units 'second' used to set field 'field' (allowed: 'meter').

.. note::

   The same unit registry must be used to define field units and interpret 
   dictionaries.

If the magnitude entry is already a Pint quantity, conversion to passed units
will be performed (and will fail if incompatible units are detected):

.. doctest::

   >>> pinttr.interpret_units({"field": 1.0 * ureg.m, "field_units": "km"}, ureg)
   {'field': <Quantity(0.001, 'kilometer')>}
   >>> pinttr.interpret_units({"field": 1.0 * ureg.s, "field_units": "m"}, ureg)
   Traceback (most recent call last):
       ...
   pint.errors.DimensionalityError: Cannot convert from 'second' ([time]) to 'meter' ([length])
