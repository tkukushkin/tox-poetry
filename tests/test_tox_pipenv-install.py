# coding: utf-8
import pytest
from tox.venv import tox_testenv_create

from tox_poetry import tox_testenv_install_deps


def test_foo():
    assert True


@pytest.mark.skip()
def test_install_deps_indexserver(newmocksession):
    mocksession = newmocksession(
        [],
        """\
        [tox]
        [testenv:py123]
        deps=
            dep1
        """,
    )
    venv = mocksession.getvenv("py123")
    with mocksession.newaction(venv.name, "getenv") as action:
        tox_testenv_create(action=action, venv=venv)
        pcalls = mocksession._pcalls
        assert len(pcalls) == 1
        pcalls[:] = []

        it = tox_testenv_install_deps(action=action, venv=venv)
        next(it)
        next(it, None)

        assert len(pcalls) == 1
        args = " ".join(pcalls[0].args)
        assert args.endswith('/poetry install')
