Changelog
=========

.. image:: https://img.shields.io/badge/calver-YY.MINOR.MICRO-blue?style=flat-square
   :target: https://calver.org/

.. towncrier release notes start

21.2.0 (2021-04-26)
-------------------

* ``pinttr.UnitContext``: Added square bracket syntax.

21.1.0 (2021-03-08)
-------------------

* ``pinttr.converters.ensure_units()``: Moved to ``pinttr.util``.

Developer-side changes
^^^^^^^^^^^^^^^^^^^^^^

* Switched to calendar versioning (schema: YY.MINOR.MICRO).

1.1.0 (2021-02-18)
------------------

* ``pinttr.interpret_units()``: Support for ``pint.Quantity`` magnitude values.
* ``pinttr.UnitContext``: Added custom unit registry for string-to-units
  interpretation.

Developer-side changes
^^^^^^^^^^^^^^^^^^^^^^

* Set up bump2version to help with version number management.
* Raised test coverage to 100%.
* Upgraded dependency pinning system for cleaner environment setup and update.

1.0.0 (2021-02-04)
------------------

Initial release.
