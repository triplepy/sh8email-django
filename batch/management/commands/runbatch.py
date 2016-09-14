import os
import signal

from django.conf import settings
from django.core.management import BaseCommand

from batch.maildelete import MailDeleteBatch


class Command(BaseCommand):
    help = 'Run mail delete batch server.'

    def __init__(self):
        super().__init__()
        self.pid_file_path = os.path.join(settings.BASE_DIR, 'tmp', 'pids', 'runbatch.pid')

    def add_arguments(self, parser):
        parser.add_argument('--stop', action='store_true', help='Stop the mail delete batch server.')

    def handle(self, *args, **options):
        if options['stop']:
            self.stop_process()
        else:
            self.start_process()

    def start_process(self):
        print("BATCH JOB SCHEDULE IS START")
        p = MailDeleteBatch()
        p.start()
        print("BATCH JOB SCHEDULE IS STARTED")
        self.store_pid(p)

    def store_pid(self, p):
        with open(self.pid_file_path, 'w') as f:
            f.write(str(p.pid))

    def stop_process(self):
        if not os.path.isfile(self.pid_file_path):
            print("There is no running process of mail delete batch server to stop.")
            return

        with open(self.pid_file_path) as f:
            pid = f.read()
        pid = int(pid)

        os.kill(pid, signal.SIGTERM)
        print("BATCH JOB SCHEDULE IS STOPPED")

        os.remove(self.pid_file_path)
