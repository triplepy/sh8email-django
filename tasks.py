from invoke import Collection
from invoke import task

from invoke_tasks import test


@task
def deploy(ctx):
    ctx.run("git pull")
    ctx.run("python manage.py collectstatic --noinput")
    ctx.run("touch ../reload")


namespace = Collection(deploy, test)
