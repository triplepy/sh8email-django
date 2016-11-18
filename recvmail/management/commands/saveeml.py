import sys, tempfile, os
from subprocess import call

from django.core.management import BaseCommand

from ...msgparse import raw_to_mail


class Command(BaseCommand):
    help = 'Save the raw email to DB after convert it to Mail object.'
    EDITOR = os.environ.get('EDITOR', 'nano')
    initial_msg = "Replace this message with the raw email message."

    def handle(self, *args, **options):
        with tempfile.NamedTemporaryFile(suffix=".tmp") as f:
            f.write(bytes(self.initial_msg, encoding='utf-8'))
            f.flush()
            call([self.EDITOR, f.name])
            f.seek(0)

            raw = str(f.read(), encoding='utf-8')
            mail = raw_to_mail(raw)
            mail.save()

            if mail.id is not None:
                print("Succeded.")
            else:
                print("Failed.")
