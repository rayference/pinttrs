.. _api_classic:

API Reference (classic)
=======================

.. currentmodule:: pinttr

.. _api_classic-main:

Main interface
--------------

.. autofunction:: pinttr.ib

.. _api_classic-dynamic:

Dynamic unit management
-----------------------

.. autoclass:: pinttr.UnitGenerator
   :members:
   :special-members: __call__

.. autoclass:: pinttr.UnitContext
   :members:
   :special-members: __getitem__, __setitem__

.. _api_classic-unit_registry:

Default unit registry
---------------------

.. autofunction:: pinttr.get_unit_registry
.. autofunction:: pinttr.set_unit_registry

.. _api_classic-dict_interpretation:

Dictionary interpretation
-------------------------

.. autofunction:: pinttr.interpret_units

.. _api_classic-converters:

Converters [``pinttr.converters``]
----------------------------------

.. autofunction:: pinttr.converters.to_units

.. _api_classic-validators:

Validators [``pinttr.validators``]
----------------------------------

.. autofunction:: pinttr.validators.has_compatible_units

.. _api_classic-utilities:

Utilities [``pinttr.util``]
---------------------------

.. autofunction:: pinttr.util.always_iterable
.. autofunction:: pinttr.converters.ensure_units
.. autofunction:: pinttr.util.units_compatible

.. _api_classic-exceptions:

Exceptions [``pinttr.exceptions``]
----------------------------------

.. autoexception:: pinttr.exceptions.UnitsError
   :show-inheritance:
