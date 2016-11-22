import sys
import time
from urllib.request import urlopen
from invoke import Collection
from invoke import task

from invoke_tasks import test
from invoke_tasks.helpers import is_task_file_changed


@task
def deploy(ctx):
    pull_result = ctx.run("git pull")
    if is_task_file_changed(pull_result):
        sys.exit("Pyinvoke task file(s) is changed. Please re-run this task.")
    ctx.run("pip install -r requirements.txt")
    ctx.run("python manage.py makemigrations")
    ctx.run("python manage.py migrate")
    ctx.run("python manage.py collectstatic --noinput")
    ctx.run("touch ../reload")
    ctx.run("sudo restart sh8recv", pty=True)
    ctx.run("sudo restart sh8batch", pty=True)
    time.sleep(1)

    with urlopen("https://sh8.email") as response:
        if not response.getcode() == 200:
            sys.exit("CRITICAL: The site respond CODE " + response.getcode())

    print("Deploy succeded.")


namespace = Collection(deploy, test)
