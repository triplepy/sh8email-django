import sys, tempfile, os
from subprocess import call

from django.core.management import BaseCommand

from ...msgparse import raw_to_mail


class Command(BaseCommand):
    help = 'Save the raw email to DB after convert it to Mail object.'
    EDITOR = os.environ.get('EDITOR', 'nano')
    initial_msg = "Replace this message with the raw email message."

    def handle(self, *args, **options):
        with tempfile.NamedTemporaryFile(suffix=".tmp", encoding="utf-8", mode="w+") as f:
            f.write(self.initial_msg)
            f.flush()

            editor_args = self.EDITOR.split() + [f.name]
            call(editor_args)

            f.seek(0)
            raw = f.read()
            
            mail = raw_to_mail(raw)
            mail.save()

            if mail.id is not None:
                print("Succeded.")
            else:
                print("Failed.")
