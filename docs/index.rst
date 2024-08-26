:hide-toc:

Pinttrs
=======

Pinttrs v\ |release|.

.. image:: https://img.shields.io/pypi/v/pinttrs?color=blue
   :target: https://pypi.org/project/pinttrs

.. image:: https://img.shields.io/conda/v/conda-forge/pinttrs?color=blue
   :target: https://anaconda.org/conda-forge/pinttrs

.. image:: https://img.shields.io/github/actions/workflow/status/leroyvn/pinttrs/ci.yml?branch=main
   :target: https://github.com/leroyvn/pinttrs/actions/workflows/ci.yml

.. image:: https://img.shields.io/readthedocs/pinttrs
   :target: https://pinttrs.readthedocs.io

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/mitsuhiko/rye/main/artwork/badge.json
    :target: https://rye-up.com
    :alt: Rye

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. image:: https://img.shields.io/badge/code%20style-black-black
   :target: https://github.com/psf/black

*Pint meets attrs.*

Pinttrs provides tools to bring extra functionality to your *attrs* classes
using Pint_.

.. _attrs: https://www.attrs.org/
.. _Pint: https://pint.readthedocs.io/

Motivation
----------

The amazing attrs_ library is a game-changer when it comes to writing classes.
Its initialisation sequence notably allows for automated conversion and
verification of attribute values. This package is an attempt at designing a
system to apply units automatically and reliably to attributes with Pint_.

Features
--------

- :ref:`Attach automatically units to unitless values passed to initialise an attribute <usage-attach_units>`
- :ref:`Verify unit compatibility when assigning a value to an attribute <usage-attach_units-validators_converters>`
- :ref:`Interpret units in dictionaries with a simple syntax <usage-interpret_dicts>`
- :ref:`Define unit context to vary unitless value interpretation dynamically <usage-unit_contexts>`

Getting started
---------------

Install from PyPI in your virtual environment:

.. code-block:: bash

   python -m pip install pinttrs

Using Conda:

.. code-block:: bash

   conda install -c conda-forge pinttrs

The :ref:`usage` section presents Pinttrs's features and how to use them.

License
-------

Pinttrs is distributed under the terms of the
`MIT license <https://choosealicense.com/licenses/mit/>`_.

About
-----

Pinttrs is written and maintained by `Vincent Leroy <https://github.com/leroyvn>`_.

Development is supported by `Rayference <https://www.rayference.eu>`_.

Pinttrs is a component of the
`Eradiate radiative transfer model <https://www.eradiate.eu>`_.

The Pinttrs logo is based on
`Agus Nugroho <https://www.iconfinder.com/nugrohoagus>`_'s glass icon and parts of
the *attrs* logo.

.. toctree::
   :caption: Use
   :hidden:

   rst/usage
   rst/compatible

.. toctree::
   :caption: Reference
   :hidden:

   rst/api
   rst/api_classic
   rst/interface
   src/whats_new.md

.. toctree::
   :caption: Develop
   :hidden:

   src/contributing.md
   GitHub repository <https://github.com/leroyvn/pinttrs>
