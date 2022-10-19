import base64
import hashlib
import os.path
import re
import subprocess
import sys

import pluggy
import toml
from tox.exception import InvocationError


_hookimpl = pluggy.HookimplMarker('tox')

_is_poetry_project = False


def get_env_name(name, cwd):
    name = name.lower()
    name = name.replace('.', '-')
    sanitized_name = re.sub(r'[ $`!*@"\\\r\n\t]', "_", name)[:42]
    normalized_cwd = os.path.normcase(os.path.realpath(cwd))
    h_bytes = hashlib.sha256(normalized_cwd.encode('utf-8')).digest()
    h_str = base64.urlsafe_b64encode(h_bytes).decode('utf-8')[:8]

    return f"{sanitized_name}-{h_str}"

@_hookimpl
def tox_addoption(parser):
    parser.add_testenv_attribute(
        "skip_poetry", "bool", "Disable poetry install", False,
    )


@_hookimpl(hookwrapper=True)
def tox_configure(config):
    yield

    pyproject_toml_path = config.toxinidir.join('pyproject.toml')
    if not pyproject_toml_path.exists():
        return

    pyproject = toml.loads(pyproject_toml_path.read())
    build_backend = pyproject.get('build-system', {}).get('build-backend')
    if build_backend not in ['poetry.masonry.api', 'poetry.core.masonry.api']:
        return

    name = pyproject['tool']['poetry']['name']
    venv_prefix = get_env_name(name, config.toxinidir)
    for envconfig in config.envconfigs.values():
        suffix = '.'.join(map(str, envconfig.python_info.version_info[:2]))
        venv_name = f'{venv_prefix}-py{suffix}'
        envconfig.envdir = config.toxworkdir / venv_name

    global _is_poetry_project  # pylint: disable=global-statement
    _is_poetry_project = True

    config.skipsdist = True


@_hookimpl()
def tox_testenv_create(venv, action):
    interp = venv.getsupportedinterpreter()
    env = venv._get_os_environ()  # pylint: disable=protected-access
    env["PYTHONIOENCODING"] = "UTF-8"
    env["POETRY_VIRTUALENVS_PATH"] = venv.envconfig.config.toxworkdir
    venv._pcall(
        [
             interp, '-m', 'poetry', 'env', 'use', interp,
        ],
        action=action,
        cwd=venv.envconfig.config.toxinidir,
        env=env,
    )


@_hookimpl(hookwrapper=True)
def tox_testenv_install_deps(venv, action):
    yield

    if not _is_poetry_project or venv.envconfig.skip_poetry is True:
        return

    cmd = [venv.getsupportedinterpreter(), '-m', 'poetry']
    cmd.append("install")
    for extra in venv.envconfig.extras:
        cmd += ['-E', extra]

    action.setactivity('installdeps', ' '.join(cmd))
    # Force UTF-8 encoding, since tox log parser epxects this (~ tox\action.py", line 128, in popen).
    env = venv._get_os_environ()  # pylint: disable=protected-access
    env["PYTHONIOENCODING"] = "UTF-8"
    env["POETRY_VIRTUALENVS_PATH"] = venv.envconfig.config.toxworkdir
    venv._pcall(  # pylint: disable=protected-access
        cmd,
        action=action,
        cwd=venv.envconfig.config.toxinidir,
        env=env,
    )
