import os
import signal

from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone


class ProcessCommand(BaseCommand):
    def __init__(self):
        super().__init__()
        self.pid_file_dir = os.path.join(settings.BASE_DIR, 'tmp', 'pids')
        self.pid_file_path = os.path.join(self.pid_file_dir, self.pid_file_name)

    def add_arguments(self, parser):
        parser.add_argument('--stop', action='store_true', help='Stop the process.')

    def handle(self, *args, **options):
        if options['stop']:
            self.stop_process()
        else:
            self.start_process()

    def start_process(self):
        p = self.process_class()
        p.start()
        self._print_with_timestamp("{} IS STARTED".format(self.process_class.__name__))
        self.store_pid(p)

    def store_pid(self, p):
        self._ensure_pids_dir_exists()
        with open(self.pid_file_path, 'w') as f:
            f.write(str(p.pid))

    def _ensure_pids_dir_exists(self):
        if not os.path.isdir(self.pid_file_dir):
            os.makedirs(self.pid_file_dir)

    def stop_process(self):
        if not os.path.isfile(self.pid_file_path):
            self._print_with_timestamp("There is no running process to stop.")
            return

        os.kill(self._read_pid(), signal.SIGTERM)
        self._print_with_timestamp("{} IS STOPPED".format(self.process_class.__name__))

        os.remove(self.pid_file_path)

    def _read_pid(self):
        with open(self.pid_file_path) as f:
            pid = f.read()
        return int(pid)

    def _print_with_timestamp(self, msg):
        print("[{}] {}".format(timezone.now().isoformat(), msg))
