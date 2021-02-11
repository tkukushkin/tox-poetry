import pluggy
import toml


hook_impl = pluggy.HookimplMarker('tox')


@hook_impl(hookwrapper=True)
def tox_testenv_install_deps(venv, action):
    yield

    project_root = venv.envconfig.config.toxinidir

    pyproject_toml_path = project_root.join('pyproject.toml')
    if not pyproject_toml_path.exists():
        return

    pyproject = toml.loads(pyproject_toml_path.read())
    build_backend = pyproject.get('build-system', {}).get('build-backend')
    if build_backend not in ['poetry.masonry.api', 'poetry.core.masonry.api']:
        return

    cmd = [
        venv.getcommandpath('poetry', venv=False),
        'install',
    ]
    for extra in venv.envconfig.extras:
        cmd += ['--extras', extra]

    action.setactivity('installdeps', ' '.join(cmd))
    venv._pcall(  # pylint: disable=protected-access
        cmd,
        action=action,
        cwd=project_root,
    )
