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
   :noindex:
   :members:
   :special-members: __call__

.. autoclass:: pinttr.UnitContext
   :noindex:
   :members:
   :special-members: __getitem__, __setitem__

.. _api_classic-unit_registry:

Default unit registry
---------------------

.. autofunction:: pinttr.get_unit_registry
   :noindex:

.. autofunction:: pinttr.set_unit_registry
   :noindex:

.. _api_classic-dict_interpretation:

Dictionary interpretation
-------------------------

.. autofunction:: pinttr.interpret_units
   :noindex:

.. _api_classic-converters:

Converters [``pinttr.converters``]
----------------------------------

.. autofunction:: pinttr.converters.to_units
   :noindex:

.. _api_classic-validators:

Validators [``pinttr.validators``]
----------------------------------

.. autofunction:: pinttr.validators.has_compatible_units
   :noindex:

.. _api_classic-utilities:

Utilities [``pinttr.util``]
---------------------------

.. autofunction:: pinttr.util.always_iterable
   :noindex:

.. autofunction:: pinttr.converters.ensure_units
   :noindex:

.. autofunction:: pinttr.util.units_compatible
   :noindex:

.. _api_classic-exceptions:

Exceptions [``pinttr.exceptions``]
----------------------------------

.. autoexception:: pinttr.exceptions.UnitsError
   :show-inheritance:
   :noindex:
