from invoke import Collection
from invoke import task

from invoke_tasks import test


def print_banner(command):
    print("============= RUN {} ===============".format(command))


@task
def deploy(ctx):
    print_banner("git pull")
    ctx.run("git pull")
    print_banner("pip install -r requirements.txt")
    ctx.run("pip install -r requirements.txt")
    print_banner("python manage.py collectstatic --noinput")
    ctx.run("python manage.py collectstatic --noinput")
    print_banner("touch ../reload")
    ctx.run("touch ../reload")


namespace = Collection(deploy, test)
