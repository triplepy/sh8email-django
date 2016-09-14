import os
import signal

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from recvmail.recv_server import Sh8MailProcess


class Command(BaseCommand):
    help = 'Run mail receiving server.'

    def __init__(self):
        super().__init__()
        self.pid_file_path = os.path.join(settings.BASE_DIR, 'tmp', 'pids', 'runrecv.pid')

    def add_arguments(self, parser):
        parser.add_argument('--stop', action='store_true', help='Stop the mail receiving server.')

    def handle(self, *args, **options):
        if options['stop']:
            self.stop_process()
        else:
            self.start_process()

    def start_process(self):
        print("SH8EMAIL SMTP SERVER IS START")
        p = Sh8MailProcess()
        p.start()
        print("SH8EMAIL SMTP SERVER IS STARTED")
        self.store_pid(p)

    def store_pid(self, p):
        with open(self.pid_file_path, 'w') as f:
            f.write(str(p.pid))

    def stop_process(self):
        if not os.path.isfile(self.pid_file_path):
            print("There is no running process of mail receiving server to stop.")
            return

        with open(self.pid_file_path) as f:
            pid = f.read()
        pid = int(pid)

        os.kill(pid, signal.SIGTERM)
        print("SH8EMAIL SMTP SERVER IS STOPPED")

        os.remove(self.pid_file_path)
