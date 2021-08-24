import sys

import pluggy
import toml
from tox.exception import InvocationError


_hookimpl = pluggy.HookimplMarker('tox')

_is_poetry_project = False


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

    global _is_poetry_project  # pylint: disable=global-statement
    _is_poetry_project = True

    config.skipsdist = True


@_hookimpl(hookwrapper=True)
def tox_testenv_install_deps(venv, action):
    yield

    if not _is_poetry_project:
        return

    project_root = venv.envconfig.config.toxinidir

    cmd = []
    try:
        cmd.append(venv.getcommandpath('poetry', venv=False))
    except InvocationError:
        cmd.append(sys.executable)
        cmd.append("-m")
        cmd.append("poetry")

    cmd.append("install")
    for extra in venv.envconfig.extras:
        cmd += ['-E', extra]

    action.setactivity('installdeps', ' '.join(cmd))
    # Force UTF-8 encoding, since tox log parser epxects this (~ tox\action.py", line 128, in popen).
    env = venv._get_os_environ()  # pylint: disable=protected-access
    env["PYTHONIOENCODING"] = "UTF-8"
    venv._pcall(  # pylint: disable=protected-access
        cmd,
        action=action,
        cwd=project_root,
        env=env,
    )
