.. _dev:

Developer guide
===============

Changelog management
--------------------

We use `Towncrier <https://github.com/twisted/towncrier>`_ to automate changelog
management. This utility collects news fragments versioned in the ``changes``
directory and generates a changelog entry from them, then updates
``CHANGELOG.rst``. News fragments are consumed and automatically removed from
versioning when used to create a changelog entry.

News fragment format:

* The filename should be ``<issue_or_hash>.<category>``.
* Supported categories are:

  * feature;
  * bugfix;
  * removal;
  * dev.

* File content should contain a brief description of the changes made.

To update the changelog during release preparation, just call

.. code-block:: bash

   towncrier build

Dependency management (Poetry)
------------------------------

*I want to ...*

**... initialise a development environment**
   Use `Poetry's environment initialisation command <https://python-poetry.org/docs/cli/#install>`_:

   .. code-block:: bash

      poetry install

   See Poetry docs if you want more control on the installation process.

**... lock dependencies**
   Use `Poetry's dependency lock command <https://python-poetry.org/docs/cli/#lock>`_:

   .. code-block:: bash

      poetry lock

   .. note:: When updating dependencies, both Conda and Poetry lock files should
      be updated. The ``lock`` make target serves that purpose:

      .. code-block:: bash

         make lock

**... update my environment based on the lock file**
   After updating locked dependencies, you can update your development environment
   using `Poetry's dependency lock command <https://python-poetry.org/docs/cli/#lock>`_:

   .. code-block:: bash

      poetry lock

   If you want to automatically add a lock file update as well:

   .. code-block:: bash

      poetry update

Dependency management (Conda)
-----------------------------

*I want to ...*

**... initialise a new development environment**
   Create a new Conda empty environment:

   .. code-block:: bash

      conda create --name <YOUR_ENV>

   Activate your environment, then initialise it:

   .. code-block:: bash

      make conda-init

   The appropriate Conda lock file should be selected based on the platform
   detected by the Makefile.

**... lock dependencies**
   The conda-lock utility is used to solve dependencies using Conda and lock
   them. A convenience make target is defined to automate the process:

   .. code-block:: bash

      make conda-lock

   To update for all platforms:

   .. code-block:: bash

      make conda-lock-all

   .. note:: When updating dependencies, both Conda and Poetry lock files should
      be updated. The ``lock`` make target serves that purpose:

      .. code-block:: bash

         make lock

**... update my environment based on the lock file**
   After updating locked dependencies, you can update your development environment
   using one of the generate lock files:

   .. code-block:: bash

      make conda-init

   If you want to automatically add a lock file update as well:

   .. code-block:: bash

      make conda-update

Publishing
----------

*I want to ...*

**... bump the version number**
   We use `bump2version <https://github.com/c4urself/bump2version>`_ for that.
   It should be included in the development environment.

   .. warning:: Always try version bump commands in dry run mode!

   .. code:: bash

      bump2version <year|minor|micro|release|build>

   Update from YY.MINOR.MICRO-<release><build> to YY.MINOR.MICRO:

   .. code:: bash

      bump2version release

   Update from YY.MINOR.MICRO-<release><build> to YY.MINOR.MICRO-<release><build+1>:

   .. code:: bash

      bump2version build

   .. note:: The ``--new-version`` option overrides the target version value.

**... update the changelog**
  Let Towncrier do the job:

  .. code-block:: bash

     towncrier build

**... create a release on GitHub**
   1. Make sure that the `GitHub CLI <https://cli.github.com/>`_ is installed on
      your machine.
   2. Ensure that the version number is set to the appropriate value.
   3. Check the changelog.
   4. Create the release:

      .. code:: bash

         gh release create v$(python3 -c "import pinttr; print(pinttr.__version__)")

      Feel free to add more options to the command if relevant.
   5. [Optional] Bump the version number to the next relevant value.

**... publish the package to PyPI**
   1. Checkout the commit corresponding to the source you want to package.
   2. [Optional] If you want your build directories to be clean, then execute:

      .. code-block:: bash

         make dist-clean

   2. Grab your PyPI credentials and simply execute:

      .. code-block:: bash

         make upload-pypi

      .. note:: This make target will also execute the ``dist`` target.

**... publish the package to Anaconda Cloud**
   We don't yet provide a conda-build recipe yet.

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


Roadmap
-------

**21.3.0**
    * Support `new-style attrs API <https://www.attrs.org/en/stable/api.html#next-generation-apis>`_.

**Not planned yet**
    * Automate packaging and publish to conda-forge instead of a private channel
      on Anaconda Cloud.
