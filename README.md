# Pintext

*Extend Pint with unit contexts*

[![PyPI version](https://img.shields.io/pypi/v/pintext?color=blue)](https://pypi.org/project/pintext)

[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/rayference/pintext/ci.yml?branch=main)](https://github.com/rayference/pintext/actions/workflows/ci.yml)
[![Documentation Status](https://img.shields.io/readthedocs/pintext)](https://pintext.readthedocs.io)

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Motivation

Scientific applications routinely accept plain numbers, *e.g.* from
configuration files, user input or serialized data. They then have to decide
what units those numbers carry. Hard-coding the answer at each site is brittle;
passing units around explicitly is noisy.

Pintext's answer is the **unit context**: a registry of named, overridable unit
generators built on [Pint](https://pint.readthedocs.io). Units are resolved when
a value is interpreted, not when the code declaring it was written, so a single
`with` block can change how an entire object tree reads its inputs.

## Features

- Define unit contexts to vary unitless value interpretation dynamically
- Attach units to unitless values and check unit compatibility with a check
  stricter than Pint's dimensionality (*e.g.* angles, radiance vs irradiance)
- Interpret quantities stored as dictionaries or xarray DataArrays
- Attach units to [attrs](https://www.attrs.org) fields
- Attach units to [pydantic](https://docs.pydantic.dev) fields

The core depends on Pint alone; the class-framework integrations are optional.

## Installation

```bash
python -m pip install pintext
python -m pip install "pintext[attrs]"  # attrs integration
python -m pip install "pintext[pydantic]"  # pydantic integration
```

Check the [documentation](https://pintext.readthedocs.io) for more detail.

## Contributing

Please refer to the
[contributor's guide](https://pintext.readthedocs.io/latest/dev.html) for the AI
usage policy, development setup instructions and development practices.

## License

Pintext is distributed under the terms of the
[MIT license](https://choosealicense.com/licenses/mit/).

## About

Pintext is written and maintained by [Vincent Leroy](https://github.com/leroyvn).

Development is supported by [Rayference](https://www.rayference.eu).

Pintext is a component of the
[Eradiate radiative transfer model](https://www.eradiate.eu).

Pintext was previously released as
[Pinttrs](https://pypi.org/project/pinttrs), which it supersedes. Pintext contains breaking changes, see the
[porting guide](https://pintext.readthedocs.io/en/latest/porting.html) for details.
