
.. _usage-interface:

About the Pinttrs interface
===========================

.. admonition:: TL;DR
   :class: note

   * As of Pinttrs v23.2.0, using the modern APIs is recommended. The classic APIs are, however, still available.
   * As of Pinttrs v23.2.0, using `import attrs` is recommended. The classic `import attr` is still supported.

Pinttrs initially mimicked the ``attrs`` import and interface policies so
that using it would feel natural to ``attrs`` users. Therefore, the code was
located in a ``pinttr`` package, and the main interface was :func:`pinttr.ib`.
Typically, a field definition would look like this:

.. doctest::

   >>> import attr, pinttr
   >>> ureg = pinttr.get_unit_registry()
   >>> @attr.s
   ... class MyClass:
   ...     field = pinttr.ib(units=ureg.m)
   >>> MyClass(1.0)
   MyClass(field=1.0 m)

As mentioned in the `documentation <https://www.attrs.org/en/latest/names.html>`_,
the ``attrs`` interface then evolved. Pinttrs followed the movement in order
to provide similar expressiveness. Consequently, we introduced :class:`pinttrs.field` and the ``pinttrs`` package:

.. doctest::

   >>> import attrs, pinttrs
   >>> @attrs.define
   ... class MyClass:
   ...     field = pinttrs.field(units=ureg.m)
   >>> MyClass(1.0)
   MyClass(field=1.0 m)

This interface is recommended, but the classic one is still available and
supported.
