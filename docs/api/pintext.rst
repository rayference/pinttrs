``pintext``
===========

The core API depends on Pint alone.

Unit contexts
-------------

.. autoclass:: pintext.UnitGenerator
   :members:

.. autoclass:: pintext.UnitContext
   :members:

Unit registry
-------------

.. autofunction:: pintext.get_unit_registry

.. autofunction:: pintext.set_unit_registry

Converters
----------

.. autofunction:: pintext.ensure_units

.. autofunction:: pintext.to_quantity

Utilities
---------

.. autofunction:: pintext.units_compatible

.. autofunction:: pintext.check_units

Exceptions
----------

.. autoclass:: pintext.UnitsError
