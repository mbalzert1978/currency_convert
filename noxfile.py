import nox


@nox.session(python=["3.11", "3.12"])
def tests(session: nox.Session):
    session.install("-r", "requirements.txt")
    session.install("pytest")
    session.log("test_json")
    session.run("pytest")


@nox.session()
def lint(session: nox.Session):
    session.install("ruff")
    session.run("ruff", ".", "--fix")


@nox.session()
def formating(session: nox.Session):
    session.install("ruff")
    session.run(
        "ruff",
        "format",
        ".",
    )


@nox.session()
def typing(session: nox.Session):
    session.install("mypy")
    session.run("mypy", ".")


@nox.session()
def security(session: nox.Session):
    session.install("bandit")
    session.run("bandit", "-c", "pyproject.toml", "-r", "currency_convert")
