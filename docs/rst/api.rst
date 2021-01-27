.. _api:

API Reference
=============

.. currentmodule:: pinttr

Main interface
--------------

.. autofunction:: pinttr.ib

Default unit registry
---------------------

.. autofunction:: pinttr.get_unit_registry
.. autofunction:: pinttr.set_unit_registry

Dictionary interpretation
-------------------------

.. autofunction:: pinttr.interpret_units

Converters [``pinttr.converters``]
----------------------------------

.. autofunction:: pinttr.converters.ensure_units
.. autofunction:: pinttr.converters.to_units

Validators [``pinttr.validators``]
----------------------------------

.. autofunction:: pinttr.validators.has_compatible_units

Utilities [``pinttr.util``]
---------------------------

.. autofunction:: pinttr.util.always_iterable
.. autofunction:: pinttr.util.units_compatible

Exceptions [``pinttr.exceptions``]
----------------------------------

.. autoexception:: pinttr.exceptions.UnitsError