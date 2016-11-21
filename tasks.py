import sys
import time
from urllib.request import urlopen
import http
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

    time.sleep(1)

    with urlopen("https://sh8.email") as response:
        if not response.getcode() == http.HTTPStatus.OK:
            sys.exit("CRITICAL: The site respond CODE " + response.getcode())

    print("Deploy succeded.")


namespace = Collection(deploy, test)
