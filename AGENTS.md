# AGENTS.md

This file provides guidance to coding agents when working with code in this repository.

## Overview

`pintext` provides **unit contexts** for [Pint](https://pint.readthedocs.io): a
registry of named, overridable unit generators that lets an application decide
at runtime how unitless values are interpreted, without threading unit
arguments through its call stack. Integrations for
[attrs](https://www.attrs.org) and [pydantic](https://docs.pydantic.dev) build
on that core and are optional. License: MIT. Pintext is a component of the
[Eradiate radiative transfer model](https://www.eradiate.eu).

This package was previously named `pinttrs` and framed as "Pint meets attrs".
The rescope dropped the `pinttr`/`pinttrs` namespaces, the `attrib()`/`ib()`
legacy interface, and `interpret_units()` (the `*_units` dict-key suffix
mechanism). There is **no compatibility shim** — that is deliberate. Dict
interpretation is served solely by `to_quantity()`.

## Environment & dependencies

The project is managed with **uv**. The core requires Pint alone; everything
else is an extra or a dev dependency.

```bash
uv sync --all-extras     # the working environment
pre-commit install
```

Extras: `pintext[attrs]`, `pintext[pydantic]`, `pintext[all]`.

## Common commands

Tasks are defined under `[tool.taskipy.tasks]` in `pyproject.toml`.

- `uv run task test` — run the full suite (unit tests + doctests).
- `uv run task docs` / `docs-serve` / `docs-clean` — build / live-serve / clean
  the Sphinx docs.
- `uv run ruff check` / `uv run ruff format --check` — lint and format checks.
- `uv run ty check` — type check (scoped to `src/`; see `[tool.ty.src]`).
- `uvx --from 'sp-repo-review[cli]' repo-review .` — Scientific Python repo
  conventions. Deliberate exemptions live in `[tool.repo-review] ignore` in
  `pyproject.toml`; note that passing `--ignore` on the command line
  *overrides* that list rather than adding to it, so run it bare.

Run a single test: `uv run pytest tests/core/test_context.py::test_name`.

Run one layer: `uv run pytest tests/core` (needs no optional dependency),
`tests/attrs`, `tests/pydantic`.

## Architecture

Three layers, in strict dependency order:

- `src/pintext/` — the core. `UnitGenerator` (`_generator.py`) and
  `UnitContext` (`_context.py`) are the point of the package; `converters.py`
  (`ensure_units`, `to_quantity`), `util.py` (`units_compatible`,
  `check_units`), `_registry.py` (the module-global default registry) and
  `exceptions.py` support them.
- `src/pintext/attrs/` — `field()`, `has_compatible_units`, `MetadataKey`.
- `src/pintext/pydantic/` — `Units` (the annotation), `Quantity`, `quantity()`.

Both integration subpackages guard their optional import in `__init__.py` and
raise an `ImportError` naming the extra to install.

### Key conventions and gotchas

- **The core is Pint-only.** Nothing under `src/pintext/` outside `attrs/` and
  `pydantic/` may import `attrs` or `pydantic`. A dedicated CI job installs the
  package without extras and runs `tests/core`; a stray import breaks it.
- **`NOTHING` (`_sentinel.py`) replaces `attrs.NOTHING`** as the deferred-mode
  sentinel of `ensure_units`. Do not reach for `attrs.NOTHING` in the core.
- **`pintext.attrs` and `pintext.pydantic` shadow the third-party package
  names** within the tree. Absolute imports resolve to the third-party
  packages, so `import attrs` inside `src/pintext/attrs/` is correct — but
  never rely on implicit relative imports.
- **`check_units` is the single shared unit check.** `has_compatible_units` is
  a three-line attrs-signature adapter over it, and the pydantic annotation
  calls it directly. Do not duplicate the comparison.
- **`UnitsError` derives from `TypeError`**, which pydantic does not collect
  into a `ValidationError`. `pintext/pydantic/_types.py` re-raises it as a
  `ValueError`, keeping the original as `__cause__`. Keep that translation if
  you touch validation.
- **"Compatible units" is stricter than dimensionality.** `units_compatible`
  declares angles incompatible with dimensionless values, and radiance
  incompatible with irradiance, where Pint does not. See
  `docs/user_guide/units.rst`.
- **The default registry is Pint's application registry**, and `to_quantity`
  uses it implicitly — it ignores any per-context `ureg`.
- **`UnitGenerator.override()` mutates in place** and restores on exit. It is
  convenient but not thread-safe.
- **`Units` is the statically-valid pydantic spelling.**
  `Annotated[pint.Quantity, Units(ureg.m)]` type-checks; `quantity(ureg.m)` is
  a function call in an annotation, which type checkers reject (the same reason
  pydantic deprecated `conint`/`constr`). Prefer `Units` in library code and in
  tests; `quantity()` is a convenience for interactive use.
- **attrs `on_setattr=None` does not disable the setattr pipeline** — it defers
  to the class-level setting, and `attrs.define` installs one.
  `attrs.setters.NO_OP` is what opts out. `None` is still what frozen classes
  need.

## Testing

- `tests/core`, `tests/attrs`, `tests/pydantic`. The latter two carry a
  `conftest.py` with `pytest.importorskip`, so the suite degrades gracefully on
  a partial install.
- **Doctests are tests.** `--doctest-modules` runs every docstring example
  under `src/`, and `--doctest-glob='*.rst'` runs every example in `docs/`.
  Both are in `testpaths`. A docstring example that is wrong fails the build.
- The root `conftest.py` injects a doctest namespace (`ureg`, `pintext`,
  `UnitContext`, `UnitGenerator`, converters, and — guarded by `try/except
  ImportError` — `attrs`, `pydantic`, `np`, `xr`). Keep the guards: core
  doctests must run on a minimal install.
- Docstrings on module-level assignments (such as `Quantity`) are **not**
  collected by doctest. Put runnable examples for those in the docs instead.
- `filterwarnings = ["error"]` and `xfail_strict = true` are on.

## Docs

Sphinx + the [shibuya](https://shibuya.lepture.com/) theme, deployed on Read
the Docs. `docs/changelog.md` is a symlink to `../CHANGELOG.md`.
`docs/porting.rst` is the pinttrs → pintext migration guide; keep its symbol
map in step with any public-API change.
`requirements/docs.txt` is the RTD input and must be kept in sync with the docs
entries of the `dev` dependency group.

Shibuya resolves `light_logo`/`dark_logo` **relative to the documentation
root** (hence the `_static/` prefix), unlike Furo. Logo file names are keyed to
ink colour, not theme: `light_logo` is the logo shown in light mode, i.e. the
dark-ink file. Both logos are placeholders pending final artwork; keep the file
names when replacing them.

## Conventions

- Ruff for lint and format (rules `B`, `E`, `F`, `I`, `UP`; isort
  `relative-imports-order = "closest-to-furthest"`).
- reST-field docstrings (`:param x:`), not numpydoc — `sphinx_autodoc_typehints`
  is configured for them.
- Type hints in signatures, using Python 3.10 syntax (`X | Y`, builtin
  generics). `requires-python` is `>=3.10`.
- Private modules are underscore-prefixed; the public API is re-exported from
  `__init__.py`.
- Versioning is [SemVer](https://semver.org/), hand-bumped in `pyproject.toml`
  via `uv version`.
- pre-commit runs ruff (check + format), taplo (TOML) and nbstripout.
