# -*- coding: utf-8 -*-
import sys
import os
sys.path.append('..' + os.sep)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sh8email.settings")

import asyncore
import multiprocessing
import smtpd

from front.models import Mail
from recvmail.util import mail_template_to_save, nomalize_recip


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        mail = mail_template_to_save(data, mailfrom)
        self.save_mail(mail, rcpttos)

    def save_mail(self, body, rcpttos):
        while(rcpttos):
            Mail.objects.create(recipient=nomalize_recip(rcpttos.pop()),
                                sender=body['From'],
                                subject=body['Subject'],
                                contents=body.get_payload())


class Sh8MailProcess(multiprocessing.Process):
    def run(self):
        self.server = CustomSMTPServer(('0.0.0.0', 25), None)
        asyncore.loop()


if __name__ == "__main__":
    p = Sh8MailProcess()
    p.start()
