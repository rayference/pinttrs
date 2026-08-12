# Contributing

## AI usage policy

Pintext has an explicit [AI usage policy](https://github.com/rayference/pintext/blob/main/AI_POLICY.md).
Please read it before opening an issue or a pull request. Agent-specific
guidance for working in this repository lives in
[`AGENTS.md`](https://github.com/rayference/pintext/blob/main/AGENTS.md).

## Contributing to the code base

### Requirements

Developing requires:

* the [uv](https://docs.astral.sh/uv/) package manager;
* the [pre-commit](https://pre-commit.com/) git hook manager, typically
  installed with [pipx](https://pipx.pypa.io/stable/).

### Setting up a development environment

Clone the repository:

```bash
git clone git@github.com:rayference/pintext.git
```

Enter the created repository and set up the development environment:

```bash
cd pintext
uv sync --all-extras
```

Finally, activate the pre-commit hooks:

```bash
pre-commit install
```

### Package layout

Pintext is built in three layers:

* `src/pintext/` — the core, which must depend on Pint alone;
* `src/pintext/attrs/` — the *attrs* integration, behind the `attrs` extra;
* `src/pintext/pydantic/` — the *pydantic* integration, behind the `pydantic`
  extra.

**Nothing in the core may import `attrs` or `pydantic`.** A dedicated CI job
installs the package without extras and runs `tests/core`, so a stray import
breaks the build.

### Running tests

The testing process of Pintext uses [pytest](https://docs.pytest.org). A task is
defined to help you run the tests:

```bash
uv run task test
```

This runs unit tests, the doctests embedded in every docstring under `src/`,
and the doctests in the documentation. Tests are split by layer:

```bash
uv run pytest tests/core       # no optional dependency required
uv run pytest tests/attrs      # skipped without attrs
uv run pytest tests/pydantic   # skipped without pydantic
```

### Linting and type checking

```bash
uv run ruff check
uv run ruff format --check
uv run ty check
```

Repository conventions are checked with
[repo-review](https://learn.scientific-python.org/development/guides/repo-review/):

```bash
uvx --from 'sp-repo-review[cli]' repo-review .
```

Deliberate exemptions are recorded in `[tool.repo-review] ignore` in
`pyproject.toml`. Passing `--ignore` on the command line overrides that list
rather than adding to it, so run the command bare.

## Building the documentation

To build the documentation, use the dedicated task:

```bash
uv run task docs
```

Incremental autobuild is also supported:

```bash
uv run task docs-serve
```

## Maintainers: release process

Pintext follows [Semantic Versioning](https://semver.org/).

**Pre-release steps**

1. Make sure that all tests pass.
2. Make sure the change log is up-to-date. Add the release date to the relevant
   section header.
3. Set the package version number to the target value:

   ```bash
   uv version <MAJOR.MINOR.PATCH>
   ```

4. Create and push a commit with the following message:
   `pintext version <MAJOR.MINOR.PATCH>`.

**Release steps**

1. Create a
   [new release on GitHub](https://github.com/rayference/pintext/releases).
2. When asked for a tag, create a new one (`v<MAJOR.MINOR.PATCH>`).
3. The automated workflow will build the package and upload it to PyPI using
   [Trusted Publishing](https://docs.pypi.org/trusted-publishers/). No API
   token is involved; the `pypi` environment must be configured as a trusted
   publisher for the project.

**Post-release steps**

1. Create a new section in the change log (`CHANGELOG.md`) with the title
   *Pintext <MAJOR.MINOR.PATCH> (upcoming release)*.
2. Bump the version to the next development one:

   ```bash
   uv version <MAJOR.MINOR.PATCH>.dev
   ```

3. Create and push a commit with the following message:
   `Version <MAJOR.MINOR.PATCH> ready for development`.

## Roadmap

**Not planned yet**

* Nothing currently.
