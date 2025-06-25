.. _api:

API Reference
=============

.. currentmodule:: pinttrs

.. _api-main:

Main interface
--------------

.. autofunction:: pinttrs.field

.. _api-dynamic:

Dynamic unit management
-----------------------

.. autoclass:: pinttrs.UnitGenerator
   :members:
   :special-members: __call__

.. autoclass:: pinttrs.UnitContext
   :members:
   :special-members: __getitem__, __setitem__

.. _api-unit_registry:

Default unit registry
---------------------

.. autofunction:: pinttrs.get_unit_registry
.. autofunction:: pinttrs.set_unit_registry

.. _api-dict_interpretation:

Dictionary interpretation
-------------------------

.. autofunction:: pinttrs.interpret_units

.. _api-converters:

Converters [``pinttrs.converters``]
-----------------------------------

.. autofunction:: pinttrs.converters.to_units

.. _api-validators:

Validators [``pinttrs.validators``]
-----------------------------------

.. autofunction:: pinttrs.validators.has_compatible_units

.. _api-utilities:

Utilities [``pinttrs.util``]
----------------------------

.. autofunction:: pinttrs.util.always_iterable
.. autofunction:: pinttrs.converters.ensure_units
.. autofunction:: pinttrs.util.units_compatible

.. _api-exceptions:

Exceptions [``pinttrs.exceptions``]
-----------------------------------

.. autoexception:: pinttrs.exceptions.UnitsError
   :show-inheritance:
