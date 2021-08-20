Changelog
=========

.. image:: https://img.shields.io/badge/calver-YY.MINOR.MICRO-blue?style=flat-square
   :target: https://calver.org/

.. towncrier release notes start

Pinttrs 21.3.0 (2021-08-20)
---------------------------

Features
^^^^^^^^

- Add ``pinttr.field()``. (992acfa6985cead9b592aaf56c5b9ad6df7a98b8)
- ``pinttr.ib()``: Add nicer default repr.
  (d68ec4e6cb1bca945d741e80281ff9ed06e84f06)


Developer-side changes
^^^^^^^^^^^^^^^^^^^^^^

- Automate testing with GitHub actions.
  (1997a78759be1e5ce1e0d7accefb187a68f2783b)
- Manage changelog with Towncrier. (644ecc7e03d822723f0584767e83b253dafdce8c)
- Add coverage report with Codecov. (fa658d3e3e45f6b2e6d044662fa68ed016f22375)


Pinttrs 21.2.0 (2021-04-26)
---------------------------

Features
^^^^^^^^

* ``pinttr.UnitContext``: Added square bracket syntax.

Pinttrs 21.1.0 (2021-03-08)
---------------------------

Features
^^^^^^^^

* ``pinttr.converters.ensure_units()``: Moved to ``pinttr.util``.

Developer-side changes
^^^^^^^^^^^^^^^^^^^^^^

* Switched to calendar versioning (schema: YY.MINOR.MICRO).

Pinttrs 1.1.0 (2021-02-18)
--------------------------

Features
^^^^^^^^

* ``pinttr.interpret_units()``: Support for ``pint.Quantity`` magnitude values.
* ``pinttr.UnitContext``: Added custom unit registry for string-to-units
  interpretation.

Developer-side changes
^^^^^^^^^^^^^^^^^^^^^^

* Set up bump2version to help with version number management.
* Raised test coverage to 100%.
* Upgraded dependency pinning system for cleaner environment setup and update.

Pinttrs 1.0.0 (2021-02-04)
--------------------------

Initial release.
