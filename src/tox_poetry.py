import os
from typing import List

import toml
import tox
from packaging.version import parse

TOX_MAJOR_VERSION = parse(tox.__version__).major

if TOX_MAJOR_VERSION >= 4:
    from tox.config.sets import ConfigSet, EnvConfigSet
    from tox.execute.request import StdinSource
    from tox.plugin import impl
    from tox.session.state import State
    from tox.tox_env.api import ToxEnv
    from tox.tox_env.errors import Fail

    @impl
    def tox_add_env_config(env_conf: EnvConfigSet, state: State):
        if not state.conf.core.load("is_poetry_project"):
            return

        if "poetry" not in env_conf.load("allowlist_externals"):
            env_conf.load("allowlist_externals").append("poetry")

        env_conf.add_config(
            keys=["extras"],
            of_type=List[str],
            default=[],
            desc="extras to install of the target package",
        )

    @impl
    def tox_add_core_config(core_conf: ConfigSet, state: State):
        pyproject_toml_path = os.path.join(
            core_conf["tox_root"], "pyproject.toml"
        )

        if not os.path.exists(pyproject_toml_path):
            return

        with open(pyproject_toml_path, "r") as fp:
            pyproject = toml.load(fp)

        build_backend = pyproject.get("build-system", {}).get("build-backend")
        if build_backend not in [
            "poetry.masonry.api",
            "poetry.core.masonry.api",
        ]:
            return

        core_conf.add_config(
            keys=["no_package", "skipsdist"],
            of_type=bool,
            default=True,
            desc="is there any packaging involved in this project",
        )
        core_conf.add_config(
            keys=["is_poetry_project"],
            of_type=bool,
            default=True,
            desc="indicator whether the project is managed by poetry",
        )

    @impl
    def tox_before_run_commands(tox_env: ToxEnv):
        if not tox_env.core["is_poetry_project"]:
            return

        cmd = []
        try:
            out = tox_env.execute(cmd=["poetry"], stdin=StdinSource.OFF)
            assert out.exit_code == 0
            cmd.append("poetry")
        except (Fail, AssertionError):
            pass

        if not cmd:
            out = tox_env.execute(
                cmd=[
                    os.path.join(tox_env.conf.load("env_bin_dir"), "python"),
                    "-m",
                    "poetry",
                ],
                stdin=StdinSource.OFF,
            )
            out.assert_success()
            cmd.extend(
                [
                    os.path.join(tox_env.conf.load("env_bin_dir"), "python"),
                    "-m",
                    "poetry",
                ]
            )

        cmd.append("install")
        for extra in tox_env.conf["extras"]:
            cmd += ["-E", extra]

        tox_env.environment_variables["PYTHONIOENCODING"] = "UTF-8"
        tox_env.execute(cmd=cmd, stdin=StdinSource.OFF).assert_success()

else:
    import sys

    import pluggy
    from tox.exception import InvocationError

    _hookimpl = pluggy.HookimplMarker("tox")

    _is_poetry_project = False

    @_hookimpl(hookwrapper=True)
    def tox_configure(config):
        yield

        pyproject_toml_path = config.toxinidir.join("pyproject.toml")
        if not pyproject_toml_path.exists():
            return

        pyproject = toml.loads(pyproject_toml_path.read())
        build_backend = pyproject.get("build-system", {}).get("build-backend")
        if build_backend not in [
            "poetry.masonry.api",
            "poetry.core.masonry.api",
        ]:
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
            cmd.append(venv.getcommandpath("poetry", venv=False))
        except InvocationError:
            cmd.append(sys.executable)
            cmd.append("-m")
            cmd.append("poetry")

        cmd.append("install")
        for extra in venv.envconfig.extras:
            cmd += ["-E", extra]

        action.setactivity("installdeps", " ".join(cmd))
        # Force UTF-8 encoding, since tox log parser epxects this (~ tox\action.py", line 128, in popen).
        env = venv._get_os_environ()  # pylint: disable=protected-access
        env["PYTHONIOENCODING"] = "UTF-8"
        venv._pcall(  # pylint: disable=protected-access
            cmd,
            action=action,
            cwd=project_root,
            env=env,
        )
