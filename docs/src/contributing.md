# Contributing

## Contributing to the code base

### Requirements

Developing requires:

* the [Rye](https://rye-up.com/) package manager;
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
rye sync
```

Finally, activate the pre-commit hooks:

```bash
pre-commit install
```

### Running tests

The testing process of Pinttrs uses [pytest](https://docs.pytest.org). A Make target is defined to
help you run the tests:

```bash
make test
```

This will run pytest for all relevant files (unit tests and doctests included
in the documentation).

## Building the documentation

To build the documentation, use the dedicated Make target:

```bash
make docs
```

Incremental autobuild is also supported:

```bash
make docs-serve
```

## Roadmap

**Not planned yet**

* Allow automatic string interpretation using the built-in registry (this feature
  should have a switch based on a user setting).
