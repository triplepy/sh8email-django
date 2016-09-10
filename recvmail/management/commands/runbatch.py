from django.core.management import BaseCommand

from recvmail.recv_server import BatchJobSchedule


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("BATCH JOB SCHEDULE IS START")
        p = BatchJobSchedule()
        p.start()
        print("BATCH JOB SCHEDULE IS STARTED")