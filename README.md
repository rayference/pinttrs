# Pinttrs

*Pint meets attrs*

[![PyPI version](https://img.shields.io/pypi/v/pinttrs?color=blue)](https://pypi.org/project/pinttrs)
[![Conda version](https://img.shields.io/conda/v/eradiate/pinttrs?color=blue)](https://anaconda.org/eradiate/pinttrs)

[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/leroyvn/pinttrs/ci.yml?branch=main)](https://github.com/leroyvn/pinttrs/actions/workflows/ci.yml)
[![Documentation Status](https://img.shields.io/readthedocs/pinttrs)](https://pinttrs.readthedocs.io)

[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/mitsuhiko/rye/main/artwork/badge.json)](https://rye-up.com)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black?style)](https://black.readthedocs.io)

## Motivation

The amazing [`attrs`](https://www.attrs.org) library is a game-changer when it
comes to writing classes. Its initialization sequence notably allows for
automated conversion and verification of attribute values. This package is an
attempt at designing a system to apply units automatically and reliably to
attributes with [Pint](https://pint.readthedocs.io).

## Features

- Attach automatically units to unitless values passed to initialize an attribute
- Verify unit compatibility when assigning a value to an attribute
- Interpret units in dictionaries with a simple syntax
- Define unit context to vary unitless value interpretation dynamically

Check the [documentation](https://pinttrs.readthedocs.io) for more detail.

## License

Pinttrs is distributed under the terms of the
[MIT license](https://choosealicense.com/licenses/mit/).

## About

Pinttrs is written and maintained by [Vincent Leroy](https://github.com/leroyvn).

Development is supported by [Rayference](https://www.rayference.eu).

Pinttrs is a component of the
[Eradiate radiative transfer model](https://www.eradiate.eu).

The Pinttrs logo is based on
[Agus Nugroho](https://www.iconfinder.com/nugrohoagus)'s glass icon and parts of
the ``attrs`` logo.
