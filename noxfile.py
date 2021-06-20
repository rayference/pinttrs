import nox
import nox_poetry


def pytest(session):
    args = session.posargs or ["--cov=src", "--doctest-glob='*.rst'", "docs", "tests"]
    session.run("pytest", *args)


@nox_poetry.session(python=["3.6", "3.7", "3.8", "3.9"])
def test_poetry(session):
    session.run("poetry", "install", external=True)
    pytest(session)


@nox.session(venv_backend="conda", python=["3.6", "3.7", "3.8", "3.9"])
def test_poetry_conda(session):
    session.run("poetry", "install", external=True)
    pytest(session)


@nox.session(venv_backend="conda", python=["3.6", "3.7", "3.8", "3.9"])
def test_conda(session):
    session.conda_install("attrs", "pint", "pytest", "pytest-cov", "setuptools")
    session.run("python", "setup.py", "develop", "--no-deps")
    pytest(session)
