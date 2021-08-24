# coding: utf-8
import pytest
from tox.venv import tox_testenv_create

import tox_poetry
from tox_poetry import tox_testenv_install_deps


def test_install_deps_indexserver(newmocksession, monkeypatch):
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
        monkeypatch.setattr(tox_poetry, "_is_poetry_project", True)
        tox_testenv_create(action=action, venv=venv)
        pcalls = mocksession._pcalls
        assert len(pcalls) == 1
        pcalls[:] = []

        it = tox_testenv_install_deps(action=action, venv=venv)
        next(it)
        next(it, None)

        assert len(pcalls) == 1
        args = " ".join(pcalls[0].args)
        assert "poetry" in args and "install" in args
        assert pcalls[0].env["PYTHONIOENCODING"] == "UTF-8"
