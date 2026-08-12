.. _user_guide:

User guide
==========

Pintext is built in three layers:

* a **core** that depends on Pint alone and provides unit contexts, converters
  and compatibility checks;
* an **attrs integration**;
* a **pydantic integration**.

Start with :doc:`unit_contexts`. The other pages cover the supporting converters
and the two class-framework integrations.

Installation
------------

Pintext requires Python 3.10 or later. Install it from PyPI in your virtual
environment:

.. code-block:: bash

    python -m pip install pintext

The core depends on Pint. Xarray-related features work automatically if xarray
is installed. The *attrs* and *pydantic* integrations also work upon detecting
the library they are associated to. If needed, requirements for all the optional
features can be install with extras:

.. code-block:: bash

    python -m pip install "pintext[attrs]"
    python -m pip install "pintext[pydantic]"
    python -m pip install "pintext[xarray]"

.. note::
    Pintext is its continuation of Pinttrs. See the :doc:`porting guide </porting>`
    for a list of changes.

.. toctree::
    :maxdepth: 2
    :hidden:

    unit_contexts
    units
    attrs
    pydantic
