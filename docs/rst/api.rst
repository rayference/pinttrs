.. _api:

API Reference
=============

.. currentmodule:: pinttr

.. _api-main:

Main interface
--------------

.. autofunction:: pinttr.ib

.. _api-dynamic:

Dynamic unit management
-----------------------

.. autoclass:: pinttr.UnitGenerator
   :members:
   :special-members: __call__

.. autoclass:: pinttr.UnitContext
   :members:
   :special-members: __getitem__, __setitem__

.. _api-unit_registry:

Default unit registry
---------------------

.. autofunction:: pinttr.get_unit_registry
.. autofunction:: pinttr.set_unit_registry

.. _api-dict_interpretation:

Dictionary interpretation
-------------------------

.. autofunction:: pinttr.interpret_units

.. _api-converters:

Converters [``pinttr.converters``]
----------------------------------

.. autofunction:: pinttr.converters.to_units

.. _api-validators:

Validators [``pinttr.validators``]
----------------------------------

.. autofunction:: pinttr.validators.has_compatible_units

.. _api-utilities:

Utilities [``pinttr.util``]
---------------------------

.. autofunction:: pinttr.util.always_iterable
.. autofunction:: pinttr.converters.ensure_units
.. autofunction:: pinttr.util.units_compatible

.. _api-exceptions:

Exceptions [``pinttr.exceptions``]
----------------------------------

.. autoexception:: pinttr.exceptions.UnitsError
   :show-inheritance:

Next-generation APIs
--------------------

Pinttrs provides APIs matching ``attrs``
`next-generation APIs <https://www.attrs.org/en/stable/api.html#next-generation-apis>`_
for syntactic homogeneity.

.. autofunction:: pinttr.field
