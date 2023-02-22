# -- Dependency management with PDM --------------------------------------------

# Lock PDM dependencies
pdm-lock:
	pdm lock

.PHONY: pdm-lock

# -- Dependency management with Conda ------------------------------------------

# Lock conda dependencies
conda-lock:
	mkdir -p requirements
	conda-lock lock --mamba \
	    --file pyproject.toml \
	    --lockfile requirements/conda-lock.yml

# Initialise development environment
conda-init:
	conda-lock install --mamba \
	    --name pinttrs \
	    requirements/conda-lock.yml
	conda run \
	    --name pinttrs \
	    python3 -m pip install --editable --no-deps .

# Shortcut for PDM and conda lock
lock: conda-lock pdm-lock

conda-update: conda-lock conda-init lock

.PHONY: conda-lock conda-init conda-update

# -- Testing -------------------------------------------------------------------

test:
	nox --no-venv -s test

nox-test:
	nox -s test

test-clean:
	rm -f .coverage*

.PHONY: test nox-test test-clean

# -- Documentation -------------------------------------------------------------

docs:
	pdm run sphinx-build -b html docs docs/_build/html
	@echo "Access documentation at docs/_build/html/index.html"

docs-clean:
	rm -rf docs/_build/

docs-serve:
	pdm run sphinx-autobuild docs docs/_build/html

.PHONY: docs

# -- Build ---------------------------------------------------------------------

build:
	pdm build

dist-clean:
	rm -rf build dist

publish: build
	pdm publish

.PHONY: build dist-clean publish
