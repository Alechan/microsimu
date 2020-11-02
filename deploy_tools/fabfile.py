from fabric.api import cd, env, local, run
from fabric.contrib.files import exists


def deploy(git_repo, branch, server_username):
    site_folder = f'/home/{server_username}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source(git_repo, branch)
        _docker_compose_up()
        _update_static_files()
        _update_database()


def _get_latest_source(git_repo, branch):
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {git_repo} .')
    run(f'git checkout {branch}')
    run(f'git pull origin {branch}')


def _docker_compose_up():
    run('docker-compose up --build -d')


def _update_database():
        run('docker-compose exec -T web python manage.py migrate --noinput')


def _update_static_files():
    run('docker-compose exec -T web python manage.py collectstatic --noinput')
