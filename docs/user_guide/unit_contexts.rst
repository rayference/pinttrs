.. _usage-unit_contexts:

Unit contexts
=============

A unit context answers the question *"what units does this bare number carry?"*
at the moment the number is interpreted, rather than at the moment the code
reading it was written.

All examples on this page use the default unit registry, available as ``ureg``:

.. doctest::

    >>> import pintext
    >>> ureg = pintext.get_unit_registry()

.. _usage-unit_contexts-generators:

Unit generators
---------------

The building block is :class:`.UnitGenerator`: a small callable that stores
units and returns them when called.

.. doctest::

    >>> generator = pintext.UnitGenerator(ureg.m)
    >>> generator()
    <Unit('meter')>

Stored units can be modified:

.. doctest::

    >>> generator.units = ureg.s
    >>> generator()
    <Unit('second')>

Anything that accepts units in Pintext also accepts a generator. Because the
generator is *evaluated* at each use, replacing its units changes the outcome
of every site that holds a reference to it — this is the indirection the whole
package is built on.

.. doctest::

    >>> generator.units = ureg.m
    >>> converter = pintext.ensure_units(default_units=generator)
    >>> converter(1.0)
    <Quantity(1.0, 'meter')>
    >>> generator.units = ureg.km
    >>> converter(1.0)
    <Quantity(1.0, 'kilometer')>

Temporary override
^^^^^^^^^^^^^^^^^^

Assigning to ``units`` is permanent. The :meth:`.UnitGenerator.override`
context manager applies a temporary change and restores the previous value on
exit:

.. doctest::

    >>> generator = pintext.UnitGenerator(ureg.m)
    >>> with generator.override(ureg.km):
    ...     generator()
    <Unit('kilometer')>
    >>> generator()
    <Unit('meter')>

Override values may be given as strings, interpreted against the registry of
the currently stored units:

.. doctest::

    >>> with generator.override("mile"):
    ...     generator()
    <Unit('mile')>

.. note::
    :meth:`~.UnitGenerator.override` mutates the generator in-place. It is
    convenient but not thread-safe: two threads overriding the same generator
    will interfere.

Composed unit generators
^^^^^^^^^^^^^^^^^^^^^^^^

The :class:`.UnitGenerator` constructor accepts any callable, which makes it
possible to derive units from other generators:

.. doctest::

    >>> length = pintext.UnitGenerator(ureg.m)
    >>> time = pintext.UnitGenerator(ureg.s)
    >>> speed = pintext.UnitGenerator(lambda: length() / time())
    >>> speed()
    <Unit('meter / second')>

Overriding a component propagates to the composed generator:

.. doctest::

    >>> with length.override(ureg.km), time.override(ureg.hour):
    ...     speed()
    <Unit('kilometer / hour')>

.. _usage-unit_contexts-contexts:

Collecting generators in a context
----------------------------------

:class:`.UnitContext` manages a structured collection of unit generators. The
simplest definition uses a string-keyed dictionary:

.. doctest::

    >>> uctx = pintext.UnitContext({"length": pintext.UnitGenerator(ureg.m)})

Units passed directly are turned into generators automatically:

.. doctest::

    >>> uctx = pintext.UnitContext({"length": ureg.m})
    >>> uctx.deferred("length")
    UnitGenerator(units=<Unit('meter')>)

Additional entries are added with :meth:`~.UnitContext.register`:

.. doctest::

    >>> uctx.register("time", ureg.s)
    >>> uctx.get_all()
    {'length': <Unit('meter')>, 'time': <Unit('second')>}

:meth:`~.UnitContext.get` evaluates a single entry:

.. doctest::

    >>> uctx.get("length")
    <Unit('meter')>

.. note::
    :meth:`~.UnitContext.get` and :meth:`~.UnitContext.register` are aliased
    with square brackets:

    .. doctest::

        >>> uctx["time"] = ureg.ms
        >>> uctx["time"]
        <Unit('millisecond')>
        >>> uctx["time"] = pintext.UnitGenerator(ureg.s)
        >>> uctx["time"]
        <Unit('second')>

:meth:`~.UnitContext.get` returns *evaluated* units — a snapshot. To keep the
indirection, ask for the generator itself with :meth:`~.UnitContext.deferred`:

.. doctest::

   >>> uctx.deferred("length")
   UnitGenerator(units=<Unit('meter')>)

This is the object to hand to :func:`.ensure_units`, to
:func:`pintext.attrs.field` or to :func:`pintext.pydantic.quantity`.

Temporary override
^^^^^^^^^^^^^^^^^^

:meth:`.UnitContext.override` overrides several registered generators at once,
using a dictionary:

.. doctest::

    >>> with uctx.override({"length": ureg.mile, "time": ureg.hour}):
    ...     ureg.Quantity(1.0, "km/hour").to(uctx.get("length") / uctx.get("time"))
    <Quantity(0.621371192, 'mile / hour')>

or keyword arguments:

.. doctest::

    >>> with uctx.override(length=ureg.mile, time=ureg.hour):
    ...     ureg.Quantity(1.0, "km/hour").to(uctx.get("length") / uctx.get("time"))
    <Quantity(0.621371192, 'mile / hour')>

Just like :class:`.UnitGenerator`, values may be strings:

.. doctest::

    >>> with uctx.override(length="mile", time="hour"):
    ...     ureg.Quantity(1.0, "km/hour").to(uctx.get("length") / uctx.get("time"))
    <Quantity(0.621371192, 'mile / hour')>

Non-string context keys
^^^^^^^^^^^^^^^^^^^^^^^

Registry keys need not be strings. A string-valued enumeration is a common
choice:

.. doctest::

    >>> import enum
    >>> class PhysicalQuantity(enum.Enum):
    ...     LENGTH = "length"
    ...     SPEED = "speed"
    ...     TIME = "time"

Its constructor doubles as a converter:

.. doctest::

    >>> PhysicalQuantity(PhysicalQuantity.LENGTH)
    <PhysicalQuantity.LENGTH: 'length'>
    >>> PhysicalQuantity("length")
    <PhysicalQuantity.LENGTH: 'length'>

Declaring it as the context's ``key_converter`` keeps strings usable — which
also keeps the keyword-argument form of :meth:`~.UnitContext.override` working:

.. doctest::

    >>> uctx = pintext.UnitContext(key_converter=PhysicalQuantity)
    >>> uctx.register(PhysicalQuantity.LENGTH, ureg.m)
    >>> uctx.register("time", ureg.s)
    >>> uctx.deferred(PhysicalQuantity.TIME)
    UnitGenerator(units=<Unit('second')>)
    >>> uctx.register(PhysicalQuantity.SPEED, pintext.UnitGenerator(
    ...     lambda: uctx.get(PhysicalQuantity.LENGTH) /
    ...             uctx.get(PhysicalQuantity.TIME)
    ... ))
    >>> with uctx.override(length=ureg.km, time=ureg.hour):
    ...    uctx.get("speed")
    <Unit('kilometer / hour')>

Specifying units with strings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`.UnitContext` can interpret string values as Pint units and build
generators from them. The registry used is set by the ``ureg`` constructor
argument; if unset, the registry returned by :func:`.get_unit_registry` is
used.

.. doctest::

    >>> uctx = pintext.UnitContext({"length": "m", "time": "s"}, interpret_str=True)
    >>> uctx.get_all()
    {'length': <Unit('meter')>, 'time': <Unit('second')>}

.. warning::
    Pintext's default registry is generally safe to use as it is Pint's
    application registry. However, interpreting units against it can have
    unintended consequences: units from two different registries cannot be
    combined.

    .. doctest::

        >>> other_ureg = pint.UnitRegistry()
        >>> uctx.get("length") / other_ureg.m
        Traceback (most recent call last):
            ...
        ValueError: Cannot operate with Unit and Unit of different registries.
