.. _dev:

Developer guide
===============

Dependency management (Conda)
-----------------------------

*I want to ...*

.. admonition:: ... initialise a new development environment

   Create a new Conda empty environment:

   .. code-block:: bash

      conda create --name <YOUR_ENV>

   Activate your environment, then initialise it:

   .. code-block:: bash

      make conda-init PLATFORM=<YOUR_PLATFORM>

   where ``YOUR_PLATFORM`` is one of:

   * ``linux-64``
   * ``osx-64``
   * ``win-64``

.. admonition:: ... lock Conda dependencies

   The conda-lock utility is used to solve dependencies using Conda and lock 
   them. A convenience make target is defined to automate the process:

   .. code-block:: bash

      make conda-lock PLATFORM=<YOUR_PLATFORM>

   or (to update for all platforms):

   .. code-block:: bash

      make conda-lock-all

   If you also want to lock pip dependencies, then use the ``pip-compile`` 
   target:

   .. code-block:: bash

      make pip-compile

.. admonition:: ... update my environment based on the lock file

   After updating locked dependencies, you can update your development environment
   using one of the generate lock files:

   .. code-block:: bash

      make conda-init PLATFORM=<YOUR_PLATFORM>

   If you want to automatically add a lock file update as well:

   .. code-block:: bash

      make conda-update PLATFORM=<YOUR_PLATFORM>

Dependency management (Pip)
---------------------------

*I want to ...*

.. admonition:: ... initialise a development environment

   Activate the target environment and use the ``pip-init`` make target:

   .. code-block:: bash

      make pip-init

.. admonition:: ... lock dependencies

   Use the ``pip-lock`` make target:

   .. code-block:: bash

      make pip-lock

.. admonition:: ... update my environment based on the lock file

   After updating locked dependencies, you can update your development environment
   using the ``pip-init`` make target:

   .. code-block:: bash

      make pip-init

Distributing to PyPI
--------------------

*I want to ...*

.. admonition:: ... publish the package to PyPI

   Grab your PyPI credentials and simply execute:

   .. code-block:: bash

      make upload-pypi

   This make target will also execute the ``dist`` target.

Executing tests
---------------

*I want to ...*

.. admonition:: ... run the whole test suite

   Simply execute

   .. code-block:: bash

      make test

   Tests located in ``tests/`` are written with Pytest and can be executed on 
   their own with

   .. code-block:: bash

      pytest tests

   Additional tests are located in the documentation and written with doctest.
   The docs makefile provides a target to easily execute them:

   .. code-block:: bash

      cd docs
      make doctest

Building the documentation
--------------------------

*I want to ...*

.. admonition:: ... build the documentation

   Go to the ``docs`` directory and execute the usual Sphinx target:

   .. code-block:: bash

      cd docs
      make html

   The documentation will be compiled in the ``docs/_build/html`` directory.

   For convenience, a target is also defined in the top-level makefile:

   .. code-block:: bash

      make docs
