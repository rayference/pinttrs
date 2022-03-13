# Contributing

## Contributing to the code base

### Requirements

Developing  requires:

* the [PDM](https://pdm.fming.dev/) package manager (typically installed with
  [pipx](https://pypa.github.io/pipx/));
* [Nox](https://nox.thea.codes/), a test automation framework which uses Python files
  for configuration.

### IDE configuration

Follow [instructions from the PDM documentation](https://pdm.fming.dev/#use-with-ide).

### Running tests

The testing process of Pinttrs uses [pytest](https://docs.pytest.org)
and [Nox](https://nox.thea.codes). Two make targets are defined to help you run
the tests:

* `make test`: run pytest without creating a new environment (uses equivalent
  to `nox --no-venv`);
* `make nox-test`: run pytest in a virtual environment for each selected Python
  version.

### Virtual environment issues

This project uses PDM's PEP 582 support, meaning that it does not require using
a virtual environment for development.

````{warning}
We recommend [deactivating Conda's `base` environment](https://stackoverflow.com/a/54560785/3645374)
if you don't want to use a virtual environment and instead rely on PDM's PEP
582 support.
````

You may however use one if that suits you: in that case, you'll want to
configure PDM so as to use the current virtual environment as
[instructed in the PDM docs](https://pdm.fming.dev/usage/project/#working-with-a-virtualenv):

```bash
pdm config --local use_venv true
```

### Using a Conda virtual environment

Developing Pinttrs using a Conda virtual environment is supported.
To get started, initialise an empty Conda environment:

```bash
conda create --name pinttrs
```

Then activate it and initialise it:

```bash
conda activate pinttrs
make conda-init
```

```{note}
Initialisation is possible only if a conda-lock file
`requirements/conda-lock.yml` already exists. If not, you first have to generate
it using conda-lock (see [Managing dependencies](managing_dependencies)).
```

(managing_dependencies)=
## Managing dependencies

Dependencies are managed using PDM.
The [conda-lock](https://conda-incubator.github.io/conda-lock/) utility is also
configured to help create reproducible Conda lock environments. For simplicity,
dedicated Make targets lock PDM, Conda or both environments:

```bash
make pdm-lock    # lock PDM dependencies
make conda-lock  # lock Conda dependencies
make lock        # chains PDM and Conda locking
```
