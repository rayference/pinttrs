.. pinttrs documentation master file, created by
   sphinx-quickstart on Tue Jan 19 18:21:12 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pinttrs
=======

Pinttrs v\ |release|.

.. image:: https://img.shields.io/readthedocs/pinttrs?style=flat-square
   :target: https://pinttrs.readthedocs.io

.. image:: https://img.shields.io/pypi/v/pinttrs?color=blue&style=flat-square
   :target: https://pypi.org/project/pinttrs

.. image:: https://img.shields.io/conda/v/leroyv/pinttrs?color=blue&style=flat-square
   :target: https://anaconda.org/leroyv/pinttrs

.. image:: https://img.shields.io/badge/code%20style-black-black?style=flat-square
   :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat-square&labelColor=ef8336
   :target: https://pycqa.github.io/isort

*Pint meets attrs.*

Pinttrs provides tools to bring extra functionality to your |attrs|_ classes 
using Pint_.

.. |attrs| replace:: ``attrs``
.. _attrs: https://www.attrs.org/
.. _Pint: https://pint.readthedocs.io/

Getting started
---------------

Install from PyPI in your virtual environment

..

.. code-block:: bash

   python -m pip install pinttrs

Using Conda:

.. code-block:: bash

   conda install -c leroyv pinttrs -c conda-forge

The :ref:`usage` section presents Pinttrs's features and how to use them.

--------------------------------------------------------------------------------

.. toctree::
   :maxdepth: 2
   :caption: Full contents

   rst/usage
   rst/compatible
   rst/dev
   rst/api
   rst/changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
