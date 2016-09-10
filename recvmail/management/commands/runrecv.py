from django.core.management.base import BaseCommand, CommandError

from recvmail.recv_server import Sh8MailProcess


class Command(BaseCommand):
    help = 'Run mail receiving server.'

    def handle(self, *args, **options):
        p = Sh8MailProcess()
        p.start()
