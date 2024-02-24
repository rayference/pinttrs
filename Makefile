# -- Testing -------------------------------------------------------------------

test:
	rye run pytest

# -- Documentation -------------------------------------------------------------

docs:
	rye run sphinx-build -b html docs docs/_build/html
	@echo "Access documentation at docs/_build/html/index.html"

docs-clean:
	rm -rf docs/_build/

docs-serve:
	rye run sphinx-autobuild docs docs/_build/html

.PHONY: docs
