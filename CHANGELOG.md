# Release notes

## Pintext 0.1.0 (*upcoming release*)

Pinttrs is rescoped and renamed to **Pintext**. The package is now built around
unit contexts, and *attrs* integration becomes one of two optional
class-framework integrations.

While most of the semantics and components are kept, all code using Pinttrs will
require specific migration operations. See the
[porting guide](https://pintext.readthedocs.io/latest/porting.html)
for a complete symbol map and migration instructions.

**Package**

- Restructure into a Pint-only core plus optional `pintext.attrs` and
  `pintext.pydantic` subpackages. attrs is no longer a hard dependency;
  UnitContext and UnitGenerator are now dataclasses, and a
  module-private NOTHING sentinel replaces attrs.NOTHING.
- Add pydantic integration: `Units` is the annotation attaching units to
  a field, `Quantity` accepts any quantity, and `quantity()` is a
  shorthand. Dictionary input, JSON round-trips, JSON schema and unit
  contexts are supported.
- Extract `check_units()` as the framework-agnostic unit check shared by
  both integrations; `has_compatible_units` becomes a thin attrs
  adapter.
- Remove the legacy interface: the `pinttr` namespace, `attrib()`, `ib`,
  `to_units()`, the deprecated `util.ensure_units()` alias, and the
  unused `always_iterable()`.
- Remove `interpret_units()` and the `*_units` dict-key mechanism;
  `to_quantity()` is the only dictionary interpretation pattern.
- Promote `to_quantity()` and `ensure_units()` to the top-level
  namespace and ship a py.typed marker.

**Conversion**

- Generalize `to_quantity()`: all values Pint can convert are now
  handled. Unit-carrying strings are parsed and unitless values become
  dimensionless quantities. This is a breaking change: some values that
  used to pass through are now converted. Failed conversions still pass
  through, unless strict mode is requested. `TypeError` is caught
  alongside `UndefinedUnitError`, since Pint raises it for magnitudes such
  as `None`, which the passthrough contract must keep returning as-is.
  Parse failures Pint reports outside its own exception hierarchy
  (`TokenError`, `AssertionError`, `ArithmeticError`) are caught too, so
  strings such as "(", "3 +" and "1/0" honour the same contract.
- Parse string values in `ensure_units()`. Multiplying a string by units
  produced a quantity whose magnitude was the string itself, silently.
  Strings are now parsed with the default unit registry: unit-carrying
  strings become quantities, unitless ones receive the default units,
  and unparsable ones raise.
- The pydantic integration guards its `to_quantity()` call accordingly.
  Applying it to a plain magnitude would make it dimensionless and pass
  it straight through `ensure_units()`, so the field's default units
  would never apply; only serialized input (mappings, DataArrays) is
  interpreted. Strings follow `ensure_units()`, so "2" receives the
  declared units while "2 km" is parsed; unparsable strings are
  re-raised as a ValueError and hence collected
  into a ValidationError instead of crashing the caller.
- Array magnitudes serialize to JSON as arrays, as the JSON schema
  already advertised.
- `UnitContext` no longer applies its `key_converter` twice upon
  registration, which broke non-idempotent converters. Enum converters
  hid the bug, being idempotent.

**Packaging**

- Reset the version from CalVer 26.2.0.dev0 to SemVer 0.1.0.dev0.
- Drop Python 3.8 and 3.9; required Python is now 3.10 or later.
- Publish with PyPI Trusted Publishing instead of an API token.
- Drop conda-forge packaging; PyPI is the only distribution channel.
- Declare the xarray extra and make the Read the Docs build install all
  extras, so every integration is documented.

**Docs and tooling**

- Switch the Sphinx theme from Furo to shibuya and restructure the docs
  around unit contexts, with attrs and pydantic as sibling integration
  guides.
- Add a porting guide for the pinttrs-to-pintext
  migration.
- Add a CI job that installs without extras to enforce the Pint-only core, plus
  a lint job running ruff and ty.
- Add `AGENTS.md` (with `CLAUDE.md` as a symlink) and `AI_POLICY.md`.
- Update the pre-commit hooks and satisfy [sp-repo-review](https://github.com/scientific-python/repo-review).
