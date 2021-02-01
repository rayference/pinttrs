.. _dev:

Developer guide
===============

Dependency management (Conda)
-----------------------------

*I want to ...*

**... initialise a new development environment**
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

   .. warning:: 
   
      Selecting the wrong platform or running without activating the appropriate
      virtual environment may have unintended side effects.

**... lock Conda dependencies**
   The conda-lock utility is used to solve dependencies using Conda and lock 
   them. A convenience make target is defined to automate the process:
   
   .. code-block:: bash

      make conda-lock PLATFORM=<YOUR_PLATFORM>

   To update for all platforms:

   .. code-block:: bash

      make conda-lock-all

   If you also want to lock pip dependencies, then use the ``pip-compile`` 
   target:

   .. code-block:: bash

      make pip-compile

**... update my environment based on the lock file**
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

**... initialise a development environment**
   Activate the target environment and use the ``pip-init`` make target:

   .. code-block:: bash

      make pip-init

**... lock dependencies**
   Use the ``pip-lock`` make target:

   .. code-block:: bash

      make pip-lock

**... update my environment based on the lock file**
   After updating locked dependencies, you can update your development environment
   using the ``pip-init`` make target:

   .. code-block:: bash

      make pip-init

Publishing
----------

*I want to ...*

**... create a release on GitHub**
   1. Make sure that the `GitHub CLI <https://cli.github.com/>`_ is installed on
      your machine.
   2. Ensure that the version number is set to the appropriate value.
   3. Create the release:

      .. code:: bash

         gh release create v$(python3 -c "import pinttr; print(pinttr.__version__)")

      Feel free to add more options to the command if relevant.
   4. Bump the version number to the next relevant value.

**... publish the package to PyPI**
   1. Checkout the commit corresponding to the source you want to package.
   2. [Optional] If you want your build directories to be clean, then execute:

      .. code-block:: bash

         make dist-clean

   2. Grab your PyPI credentials and simply execute:

      .. code-block:: bash

         make upload-pypi

      .. note:: This make target will also execute the ``dist`` target.

Executing tests
---------------

*I want to ...*

**... run the test suite**
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

**... get a coverage report**
   Pytest automatically runs a coverage pass. After running the ``test`` target,
   you can create a HTML coverage report with the command:

   .. code-block:: bash

      coverage html

   This command will generate a HTML coverage report in the ``htmlcov``
   directory.

Building the documentation
--------------------------

*I want to ...*

**... build the documentation**
   Go to the ``docs`` directory and execute the usual Sphinx target:

   .. code-block:: bash

      cd docs
      make html

   The documentation will be compiled in the ``docs/_build/html`` directory.

   For convenience, a target is also defined in the top-level makefile:

   .. code-block:: bash

      make docs
