# tox-poetry

[![PyPI version](https://badge.fury.io/py/tox-poetry.svg)](https://pypi.org/project/tox-poetry/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tox-poetry.svg?color=green)
[![Build Status](https://github.com/tkukushkin/tox-poetry/workflows/build/badge.svg?branch=master)](https://github.com/tkukushkin/tox-poetry/actions?query=workflow%3Abuild+branch%3Amaster)
[![codecov](https://codecov.io/gh/tkukushkin/tox-poetry/branch/master/graph/badge.svg)](https://codecov.io/gh/tkukushkin/tox-poetry)

## Usage:

Install plugin:

```bash
pip install tox-poetry
```

tox.ini:

```ini
[tox]
envlist = py38
skipsdist = True

[testenv]
commands =
  pytest tests/
```

Plugin installs all dependencies from pyproject.toml before running any commands. Like simple tox `deps`, poetry dependencies are installed only once when tox environment is created, you can run `tox -r` to recreate environment.

Exampel pyproject.toml:

```toml
[build-system]
requires = ["poetry>=1,<2"]
build-backend = "poetry.masonry.api"

[tool.poetry]
name = "example-app"
version = "0.1.0"
authors = []
description = ""

[tool.poetry.dependencies]
django = "*"

[tool.poetry.dev-dependencies]
pytest = "*"
```

Example output:

```
py38 recreate: /src/.tox/py38
py38 installdeps: /poetry/bin/poetry install
py38 installed: atomicwrites @ file:///pypoetry/artifacts/ca/84/dd/000dbc2864acca52a74a82da8b597c9e4778eb3fe64687a31a8095ad5f/atomicwrites-1.4.0-py2.py3-none-any.whl,attrs @ file:///pypoetry/artifacts/b7/28/6f/acdd2c0e759f1cda97abf00db7723a0ffb3a151696d8d96398aea16171/attrs-20.3.0-py2.py3-none-any.whl,Django @ file:///pypoetry/artifacts/2c/92/a3/702031af33acac0ba5b8551e05589cc106b52f094520fc0b189974b826/Django-1.11.29-py2.py3-none-any.whl,more-itertools @ file:///pypoetry/artifacts/1e/40/b5/3004e210820ef8517710ed156fa6d8585a1358fd5caf4720f2425443f8/more_itertools-7.2.0-py3-none-any.whl,packaging @ file:///pypoetry/artifacts/09/cd/29/a435224f3203dfba4af491065632910aadb6f3ddd87ce3c6590ac29e7a/packaging-20.4-py2.py3-none-any.whl,pluggy @ file:///pypoetry/artifacts/9c/e5/0b/2d64d03361a081edeb5d2ec5f286ccf9719587781fbf6822e1b6384c27/pluggy-0.13.1-py2.py3-none-any.whl,py @ file:///pypoetry/artifacts/f5/51/7d/d8aec03f59299351465053794c7b1f0e0e7a918e4a67911664f83929af/py-1.9.0-py2.py3-none-any.whl,pyparsing @ file:///pypoetry/artifacts/da/e7/3d/1780282f558e5fd157bf708b28b8ba0d08323ef6bc5b6396139ce38a0b/pyparsing-2.4.7-py2.py3-none-any.whl,pytest @ file:///pypoetry/artifacts/2d/0c/37/bc460d960d868e47170715a52c3c0431b094579b27805bb40fd5fd7da3/pytest-4.6.11-py2.py3-none-any.whl,pytz @ file:///pypoetry/artifacts/7a/8e/a2/e796ae4d320aded38d3d61817b158184888dcd18c6a4f6d6ab011a6cda/pytz-2020.4-py2.py3-none-any.whl,six @ file:///pypoetry/artifacts/be/98/c7/69fe6fea7a59659af1c6260899226129565330b1e07c9c5b3769be76bf/six-1.15.0-py2.py3-none-any.whl,wcwidth @ file:///pypoetry/artifacts/36/68/e2/7232f431072d5e8aeec124120b9a1d095d45da10311d271fac10982473/wcwidth-0.2.5-py2.py3-none-any.whl
py38 run-test-pre: PYTHONHASHSEED='966757075'
py38 run-test: commands[0] | pytest tests
```
