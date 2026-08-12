.. _porting:

Porting from Pinttrs
====================

Pintext is the continuation of `Pinttrs <https://pypi.org/project/pinttrs>`_,
rescoped around :doc:`unit contexts <user_guide/unit_contexts>`. The *attrs*
integration is now optional and lives in a dedicated namespace.

.. warning::
    **There is no compatibility shim.** The ``pinttr`` and ``pinttrs`` import
    namespaces no longer exist, and nothing is deprecated-but-working — removed
    names are simply gone. Porting is a one-time, mechanical edit; this page
    lists every change you need to make.

Installation and imports
------------------------

The distribution is renamed, and *attrs* is no longer a hard dependency — it
moved behind an extra:

.. code-block:: diff

    - pip install pinttrs
    + pip install "pintext[attrs]"

If you only use unit contexts and converters, plain ``pip install pintext``
is enough: the core depends on Pint alone.

Both former import namespaces collapse into one:

.. code-block:: diff

    - import pinttr     # the "classic" namespace
    - import pinttrs    # the "modern" namespace
    + import pintext

Symbol map
----------

Everything that survived, and where it went:

.. list-table::
    :header-rows: 1
    :widths: 45 55

    * - Pinttrs
      - Pintext
    * - ``pinttrs.UnitContext``
      - :class:`pintext.UnitContext`
    * - ``pinttrs.UnitGenerator``
      - :class:`pintext.UnitGenerator`
    * - ``pinttrs.get_unit_registry``
      - :func:`pintext.get_unit_registry`
    * - ``pinttrs.set_unit_registry``
      - :func:`pintext.set_unit_registry`
    * - ``pinttrs.converters.ensure_units``
      - :func:`pintext.ensure_units`
    * - ``pinttrs.converters.to_quantity``
      - :func:`pintext.to_quantity`
    * - ``pinttrs.util.units_compatible``
      - :func:`pintext.units_compatible`
    * - ``pinttrs.exceptions.UnitsError``
      - :class:`pintext.UnitsError`
    * - ``pinttrs.field``
      - :func:`pintext.attrs.field`
    * - ``pinttrs.validators.has_compatible_units``
      - :func:`pintext.attrs.has_compatible_units`
    * - ``pinttr._metadata.MetadataKey``
      - :class:`pintext.attrs.MetadataKey` (now public)

``to_quantity``, ``ensure_units``, ``units_compatible`` and ``UnitsError`` are
now reachable from the top level, so most imports get shorter:

.. code-block:: diff

    - from pinttrs.converters import ensure_units, to_quantity
    - from pinttrs.util import units_compatible
    + from pintext import ensure_units, to_quantity, units_compatible

Removed names
-------------

.. list-table::
    :header-rows: 1
    :widths: 40 60

    * - Removed
      - Replacement
    * - ``pinttr.attrib()``, ``pinttr.ib()``
      - :func:`pintext.attrs.field` (**keyword-only**)
    * - ``pinttrs.interpret_units()``
      - :func:`pintext.to_quantity` (see `Dictionary interpretation`_)
    * - ``pinttrs.converters.to_units(units)``
      - :func:`pintext.ensure_units(default_units=units) <pintext.ensure_units>` (deferred mode)
    * - ``pinttrs.util.ensure_units()``
      - :func:`pintext.ensure_units` (alias is gone, function is not)
    * - ``pinttrs.util.always_iterable()``
      - :func:`more_itertools.always_iterable`

The field factory
-----------------

``attrib()``/``ib()`` and ``field()`` collapse into a single keyword-only
:func:`pintext.attrs.field`. If you used the classic spelling, positional
arguments have to become keywords:

.. code-block:: diff

    - import attr, pinttr
    -
    - @attr.s
    - class MyClass:
    -     value = pinttr.ib(0.0, units=ureg.m)
    + import attrs
    + from pintext.attrs import field
    +
    + @attrs.define
    + class MyClass:
    +     value = field(default=0.0, units=ureg.m)

The ``cmp`` and ``type`` parameters of ``attrib()`` are not carried over; they
were already absent from ``field()`` and deprecated in *attrs* itself.

.. _porting-dicts:

Dictionary interpretation
-------------------------

This is the one change that is not a rename. ``interpret_units()`` read a flat
dictionary and paired each ``x_units`` key with its ``x`` sibling:

.. code-block:: python

    # Pinttrs
    interpret_units({"radius": 1.0, "radius_units": "m"}, ureg)
    # {'radius': <Quantity(1.0, 'meter')>}

Pintext drops thsi mechanism entirely: :func:`.to_quantity` works on a
**single quantity at a time**, which carries its magnitude and units together:

.. doctest::

    >>> import pintext
    >>> ureg = pintext.get_unit_registry()
    >>> pintext.to_quantity({"radius": 1.0, "radius_units": "m"})
    Traceback (most recent call last):
        ...
    ValueError: Supplied value has no magnitude
    >>> pintext.to_quantity({"value": 1.0, "units": "m"})
    <Quantity(1.0, 'meter')>

So the recommended port is to **reshape the serialized data**, nesting each
quantity instead of spreading it across sibling keys:

.. code-block:: diff

      {
    -   "radius": 1.0,
    -   "radius_units": "m",
    -   "duration": 30.0,
    -   "duration_units": "s"
    +   "radius": {"value": 1.0, "units": "m"},
    +   "duration": {"value": 30.0, "units": "s"}
      }

and to apply :func:`~pintext.to_quantity` per value:

.. doctest::

    >>> data = {
    ...     "radius": {"value": 1.0, "units": "m"},
    ...     "duration": {"value": 30.0, "units": "s"},
    ... }
    >>> {k: pintext.to_quantity(v) for k, v in data.items()}
    {'radius': <Quantity(1.0, 'meter')>, 'duration': <Quantity(30.0, 'second')>}

The nested form is self-contained: a value carries its own units, so it
survives being moved, nested or passed around on its own, and it is what the
:ref:`pydantic integration <usage-pydantic>` emits when serializing.

Keeping legacy documents readable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you cannot reshape your data — stored documents, a published format — drop
this adapter into your own code. It reproduces what ``interpret_units()`` did:

.. doctest::

    >>> import pint
    >>>
    >>> def interpret_units(d, ureg=None):
    ...     """Local replacement for the removed pinttrs.interpret_units()."""
    ...     if ureg is None:
    ...         ureg = pintext.get_unit_registry()
    ...     result = dict(d)
    ...     for units_key in [k for k in d if k.endswith("_units")]:
    ...         magnitude_key = units_key[: -len("_units")]
    ...         if magnitude_key not in result:
    ...             continue
    ...         units = result.pop(units_key)
    ...         magnitude = result[magnitude_key]
    ...         if isinstance(magnitude, pint.Quantity):
    ...             magnitude = magnitude.m_as(units)
    ...         result[magnitude_key] = ureg.Quantity(magnitude, units)
    ...     return result

It behaves as before, including converting an already-dimensional magnitude:

.. doctest::

    >>> interpret_units({"radius": 1.0, "radius_units": "m"})
    {'radius': <Quantity(1.0, 'meter')>}
    >>> interpret_units({"radius": 1.0 * ureg.m, "radius_units": "km"})
    {'radius': <Quantity(0.001, 'kilometer')>}

and leaving a ``_units`` key with no matching magnitude alone:

.. doctest::

    >>> interpret_units({"radius_units": "m"})
    {'radius_units': 'm'}

Treat it as a migration aid, not a destination: it is 15 lines you now own, and
the nested form above is the supported path.

Other behaviour changes
-----------------------

:func:`.to_quantity` **converts everything Pint can convert.** In Pinttrs, anything
that was not a mapping or a DataArray passed through unchanged. Pintext hands
those values to Pint, which parses unit-carrying strings and makes unitless
values dimensionless:

.. doctest::

    >>> pintext.to_quantity("2 m")
    <Quantity(2, 'meter')>
    >>> pintext.to_quantity(42.0)
    <Quantity(42.0, 'dimensionless')>

Values Pint cannot interpret still pass through; ``strict=True`` raises a
``ValueError`` instead. Code that applied ``to_quantity()`` indiscriminately and
relied on plain magnitudes surviving untouched must guard the call — this is
what :class:`pintext.pydantic.Units` does, so that a plain magnitude still
receives the field's default units rather than becoming dimensionless.

**The core classes are no longer attrs classes.** :class:`.UnitContext` and
:class:`.UnitGenerator` are :mod:`dataclasses`, which is what lets the core
depend on Pint alone. Their constructors, attributes and methods are unchanged,
but *attrs* introspection helpers no longer apply:

.. code-block:: diff

    - attrs.fields(UnitContext)      # raises NotAnAttrsClassError
    - attrs.evolve(generator, units=ureg.km)
    + dataclasses.fields(UnitContext)
    + dataclasses.replace(generator, units=ureg.km)

**A shared unit check is now public.** :func:`pintext.check_units` holds the
comparison that ``has_compatible_units`` used to own, in a form that does not
depend on an *attrs* attribute object. Use it if you validate units by hand:

.. doctest::

    >>> pintext.check_units(1.0 * ureg.km, ureg.m)
    >>> pintext.check_units(1.0 * ureg.s, ureg.m, name="radius")
    Traceback (most recent call last):
        ...
    pintext.exceptions.UnitsError: Cannot convert from 'second' to 'meter': incompatible units 'second' used to set field 'radius' (allowed: 'meter').

**Python 3.8 and 3.9 are no longer supported.** Pintext requires Python 3.10 or
later.

**Versioning switched from CalVer to SemVer.** Pinttrs used ``YY.MINOR.MICRO``;
Pintext starts at ``0.1.0`` and follows `Semantic Versioning
<https://semver.org/>`__. A version comparison that assumed the year prefix will
read Pintext versions as older — pin on the distribution name instead.

What is new
-----------

Porting is a good moment to pick these up:

* A :ref:`pydantic integration <usage-pydantic>`, with the same deferred-units
  behaviour as the *attrs* one, plus JSON round-trips and JSON schema.
* :func:`pintext.check_units`, described above.
* A ``py.typed`` marker, so type checkers now see Pintext's annotations.
