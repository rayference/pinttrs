# -- Dependency management with Pip --------------------------------------------

# Update packaging tools
pip-update-tools:
	pip install --upgrade pip-tools pip setuptools

# Lock pip dependencies
pip-compile:
	pip-compile --upgrade --build-isolation --generate-hashes \
	    --output-file requirements/main.txt \
	    requirements/main.in
	pip-compile --upgrade --build-isolation --generate-hashes \
	    --output-file requirements/docs.txt \
	    requirements/docs.in
	pip-compile --upgrade --build-isolation --generate-hashes \
	    --output-file requirements/tests.txt \
	    requirements/main.in requirements/tests.in
	pip-compile --upgrade --build-isolation --generate-hashes \
	    --output-file requirements/dev.txt \
	    requirements/main.in requirements/tests.in \
	    requirements/docs.in requirements/dev.in

# Lock dependencies
pip-lock: pip-update-tools pip-compile

# Initialise development environment
pip-init:
	pip install --upgrade -r requirements/dev.txt
	python setup.py develop

pip-update: pip-lock pip-init

.PHONY: pip-compile pip-update-tools pip-update-deps pip-init

# -- Dependency management with Conda ------------------------------------------

# Lock conda dependencies
conda-lock:
	python requirements/make_conda_env.py -o requirements/environment.yml --quiet
	conda-lock --file requirements/environment.yml \
	    --filename-template "requirements/environment-{platform}.lock" \
	    -p $(PLATFORM)

conda-lock-all:
	python requirements/make_conda_env.py -o requirements/environment.yml --quiet
	conda-lock --file requirements/environment.yml \
	    --filename-template "requirements/environment-{platform}.lock"

# Initialise development environment
conda-init:
	conda update --file requirements/environment-$(PLATFORM).lock
	python setup.py develop

conda-update: conda-lock-all conda-init

.PHONY: conda-lock conda-lock-all conda-init conda-update

# -- Testing -------------------------------------------------------------------

test:
	pytest --doctest-glob="*.rst" docs tests

.PHONY: test

# -- Documentation -------------------------------------------------------------

docs:
	make -C docs html

.PHONY: docs
