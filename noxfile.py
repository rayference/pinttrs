import nox
import nox_poetry


def pytest(session):
    args = session.posargs or ["--cov", "--doctest-glob='*.rst'", "docs", "tests"]
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
    session.conda_install("attrs", "pint", "pip", "pytest", "pytest-cov", "setuptools")
    session.install("--editable", ".", "--no-deps")
    pytest(session)


@nox_poetry.session(python="3.6")
def coverage(session):
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
