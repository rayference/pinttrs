# Contributing

## Contributing to the code base

### Requirements

Developing requires:

* the [uv](https://docs.astral.sh/uv/) package manager;
* the [pre-commit](https://pre-commit.com/) git hook manager, typically
  installed with [pipx](https://pipx.pypa.io/stable/).

### Setting up a development environment

Clone the repository:

```bash
git clone git@github.com:rayference/pinttrs.git
```

Enter the created repository and set up the development environment:

```bash
cd pinttrs
uv sync
```

Finally, activate the pre-commit hooks:

```bash
pre-commit install
```

### Running tests

The testing process of Pinttrs uses [pytest](https://docs.pytest.org). A task is
defined to help you run the tests:

```bash
uv run task test
```

This will run pytest for all relevant files (unit tests and doctests included
in the documentation).

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

**Pre-release steps**

1. Make sure that all tests pass.
2. Make sure the change log is up-to-date. Add the release date to the relevant
   section header.
3. Set the package version number to the target value:

   ```bash
   uv version <MAJOR.MINOR.PATCH>
   ```

4. Create and push a commit with the following message:
   `pinttrs version <MAJOR.MINOR.PATCH>`.

**Release steps**

1. Create a
   [new release on GitHub](https://github.com/rayference/pinttrs/releases).
2. When asked for a tag, create a new one (`v<MAJOR.MINOR.PATCH>`).
3. The automated workflow will build the package and upload it to PyPI.

**Post-release steps**

1. Create a new section in the change log (`CHANGELOG.md`) with the title
   *Pinttrs <MAJOR.MINOR.PATCH> (upcoming release)*.
2. Bump the version to the next development one:

   ```bash
   uv version <MAJOR.MINOR.PATCH>.dev
   ```

3. Create and push a commit with the following message:
   `Version <MAJOR.MINOR.PATCH> ready for development`.

## Roadmap

**Not planned yet**

* Allow automatic string interpretation using the built-in registry (this
  feature should have a switch based on a user setting).
