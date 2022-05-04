# What's new?

[![CalVer](https://img.shields.io/badge/calver-YY.MINOR.MICRO-blue?style=flat-square)](https://calver.org/)

## Pinttrs 22.1.0 (unreleased)

### Developer-side changes

* Move to PDM for dependency and project management.

## Pinttrs 21.3.1 (2021-09-13)

### Developer-side changes

* Fix documentation build ({ghcommit}`b3e8c1`, {ghcommit}`01e68f`).

## Pinttrs 21.3.0 (2021-08-20)

### Features

* Add ``pinttr.field()`` ({ghcommit}`992acf`).
* ``pinttr.ib()``: Add nicer default repr ({ghcommit}`d68ec4`).


### Developer-side changes

* Automate testing with GitHub actions ({ghcommit}`1997a7`).
* Manage changelog with Towncrier ({ghcommit}`644ecc`).
* Add coverage report with Codecov ({ghcommit}`fa658d`).


## Pinttrs 21.2.0 (2021-04-26)

### Features

* ``pinttr.UnitContext``: Added square bracket syntax.

## Pinttrs 21.1.0 (2021-03-08)

### Features

* ``pinttr.converters.ensure_units()``: Moved to ``pinttr.util``.

### Developer-side changes

* Switched to calendar versioning (schema: YY.MINOR.MICRO).

## Pinttrs 1.1.0 (2021-02-18)

### Features

* ``pinttr.interpret_units()``: Support for ``pint.Quantity`` magnitude values.
* ``pinttr.UnitContext``: Added custom unit registry for string-to-units interpretation.

### Developer-side changes

* Set up bump2version to help with version number management.
* Raised test coverage to 100%.
* Upgraded dependency pinning system for cleaner environment setup and update.

## Pinttrs 1.0.0 (2021-02-04)

Initial release.