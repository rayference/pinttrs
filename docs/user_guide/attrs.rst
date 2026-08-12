.. _usage-attrs:

attrs integration
=================

This extension requires that the attrs package is installed. If not done
externally in your project, it can be requested with the ``attrs`` extra:

.. code-block:: bash

    python -m pip install "pintext[attrs]"

:func:`pintext.attrs.field` mirrors :func:`attrs.field` and adds a ``units``
argument, which attaches units to a field:

.. doctest::

    >>> import attrs, pint, pintext
    >>> from pintext.attrs import field
    >>> ureg = pintext.get_unit_registry()
    >>> @attrs.define
    ... class MyClass:
    ...     value = field(units=ureg.km)
    >>> MyClass(1.0)
    MyClass(value=1.0 km)

.. note::
    If ``units`` is unset, :func:`pintext.attrs.field` behaves exactly like
    :func:`attrs.field`.

Unitless values are automatically wrapped. If a Pint quantity is passed, its
units are checked; when they are
:ref:`compatible in the sense of Pintext <compatible>`, the value is assigned
unchanged:

.. doctest::

    >>> MyClass(1.0 * ureg.m)
    MyClass(value=1.0 m)

Incompatible units make the built-in validator raise a
:class:`~pintext.exceptions.UnitsError`:

.. doctest::

    >>> MyClass(1.0 * ureg.s)
    Traceback (most recent call last):
        ...
    pintext.exceptions.UnitsError: Cannot convert from 'second' to 'kilometer': incompatible units 'second' used to set field 'value' (allowed: 'kilometer').

By default, conversion and validation also apply on assignment:

.. doctest::

    >>> o = MyClass(1.0)
    >>> o
    MyClass(value=1.0 km)
    >>> o.value = 1.0 * ureg.s
    Traceback (most recent call last):
        ...
    pintext.exceptions.UnitsError: Cannot convert from 'second' to 'kilometer': incompatible units 'second' used to set field 'value' (allowed: 'kilometer').
    >>> o.value = 1.0 * ureg.m
    >>> o
    MyClass(value=1.0 m)
    >>> o.value = 1.0
    >>> o
    MyClass(value=1.0 km)

.. note::
    To opt out, pass :obj:`attrs.setters.NO_OP`:

    .. doctest::

        >>> @attrs.define
        ... class AnotherClass:
        ...     value = field(units=ureg.km, on_setattr=attrs.setters.NO_OP)
        >>> o = AnotherClass(1.0)
        >>> o
        AnotherClass(value=1.0 km)
        >>> o.value = 1.0
        >>> o
        AnotherClass(value=1.0)

    Passing ``on_setattr=None`` is *not* equivalent: ``None`` means "defer to
    the class-level setting", and :func:`attrs.define` installs a
    convert-and-validate pipeline of its own, so conversion still happens.

    .. doctest::

        >>> @attrs.define
        ... class AnotherClass:
        ...     value = field(units=ureg.km, on_setattr=None)
        >>> o = AnotherClass(1.0)
        >>> o.value = 1.0
        >>> o
        AnotherClass(value=1.0 km)

    ``None`` is however what you need for frozen classes, which reject any
    ``on_setattr`` at all:

    .. doctest::

        >>> @attrs.frozen
        ... class AnotherClass:
        ...     value = field(units=ureg.m)
        Traceback (most recent call last):
            ...
        ValueError: Frozen classes can't use on_setattr.
        >>> @attrs.frozen
        ... class AnotherClass:
        ...     value = field(units=ureg.m, on_setattr=None)

Fields with units also get a ``repr`` suited to displaying quantities. The
original one is restored by passing ``repr=True``:

.. doctest::

    >>> @attrs.define
    ... class AnotherClass:
    ...     value = field(units=ureg.km, repr=True)
    >>> AnotherClass(1.0)
    AnotherClass(value=<Quantity(1.0, 'kilometer')>)

Unit contexts
-------------

The ``units`` argument accepts a :class:`.UnitGenerator`, so a field can read
its units from a :doc:`unit context <unit_contexts>`. Units are then resolved
at instantiation time:

.. doctest::

    >>> uctx = pintext.UnitContext({"length": ureg.m})
    >>> @attrs.define
    ... class MyClass:
    ...     value = field(units=uctx.deferred("length"))
    >>> MyClass(1.0)
    MyClass(value=1.0 m)
    >>> with uctx.override(length="km"):
    ...     MyClass(1.0)
    MyClass(value=1.0 km)

Validators and converters
-------------------------

Under the hood, :func:`~pintext.attrs.field` composes a converter
(:func:`.ensure_units` in deferred mode) and a validator
(:func:`~pintext.attrs.has_compatible_units`). Both can be used directly to
customize field behaviour further. See :doc:`/api/pintext.attrs` for details.
