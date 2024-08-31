# Release notes

[![CalVer](https://img.shields.io/badge/calver-YY.MINOR.MICRO-blue)](https://calver.org/)

## Pinttrs 24.2.0 (upcoming release)

* Pinttrs is now available on [conda-forge](https://anaconda.org/conda-forge/pinttrs).

### Developer-side changes

* Use Rye tasks instead of Makefile ({ghcommit}`beef8e`).

## Pinttrs 24.1.0 (2024-02-24)

* Add Python 3.12 support ({ghpr}`7`).
* The default registry is now the Pint application registry ({ghpr}`8`).

### Developer-side changes

* Move from PDM to Rye for project management ({ghpr}`7`).
* Drop Nox for testing ({ghpr}`7`).
* Drop Conda development environment support ({ghpr}`7`).
* Use the Ruff formatter instead of Black in pre-commit hooks ({ghpr}`7`).
* Drop Copier template ({ghpr}`7`).

## Pinttrs 23.2.0 (2023-02-25)

* Support `import pinttrs`, promote this namespace and modern APIs in documentation ({ghpr}`5`).

### Developer-side changes

* Move from isort to ruff for import sorting. This also opens the door to linting features ({ghcommit}`9a4ed0`).
* Add pre-commit hooks ({ghcommit}`5b4ab9`).

## Pinttrs 23.1.1 (2023-02-22)

*Minor release with tooling updates.*

## Pinttrs 23.1.0 (2023-02-22)

* Drop Python 3.7 support, add Python 3.11 support ({ghcommit}`191677`)

## Pinttrs 22.1.0 (2022-07-19)

### Developer-side changes

* Move to PDM for dependency and project management ({ghpr}`3`).
* Apply [Copier template](https://github.com/leroyvn/copier-pdm) for easier
  tooling management ({ghpr}`3`).
* Drop Towncrier-based changelog management ({ghpr}`3`).

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
