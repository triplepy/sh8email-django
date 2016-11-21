def is_task_file_changed(pull_result):
    task_file_paths = ["tasks.py", "invoke_tasks/"]
    for path in task_file_paths:
        if path in pull_result.stdout:
            return True
    return False
