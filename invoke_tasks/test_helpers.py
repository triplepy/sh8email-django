from unittest import TestCase
from unittest.mock import MagicMock

from .helpers import is_task_file_changed

class HelpersTest(TestCase):
    def test_is_task_file_changed__1(self):
        # given
        pull_result = MagicMock()
        pull_result_stdout = """\
remote: Counting objects: 11, done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 7 (delta 2), reused 0 (delta 0)
Unpacking objects: 100% (7/7), done.
From ssh://my.remote.host.com/~/git/myproject
 * branch            master     -> FETCH_HEAD
Updating 9d447d2..f74fb21
Fast forward
 tasks.py |   13 +++++++++++++
 1 files changed, 13 insertions(+), 0 deletions(-)
"""
        pull_result.stdout = pull_result_stdout
        # then
        self.assertTrue(is_task_file_changed(pull_result))

    def test_is_task_file_changed__2(self):
        # given
        pull_result = MagicMock()
        pull_result_stdout = """\
remote: Counting objects: 11, done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 7 (delta 2), reused 0 (delta 0)
Unpacking objects: 100% (7/7), done.
From ssh://my.remote.host.com/~/git/myproject
 * branch            master     -> FETCH_HEAD
Updating 9d447d2..f74fb21
Fast forward
 invoke_tasks/test.py |   13 +++++++++++++
 1 files changed, 13 insertions(+), 0 deletions(-)
"""
        pull_result.stdout = pull_result_stdout
        # then
        self.assertTrue(is_task_file_changed(pull_result))
