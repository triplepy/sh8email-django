from django.core.management import BaseCommand

from batch.maildelete import MailDeleteBatch


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("BATCH JOB SCHEDULE IS START")
        p = MailDeleteBatch()
        p.start()
        print("BATCH JOB SCHEDULE IS STARTED")