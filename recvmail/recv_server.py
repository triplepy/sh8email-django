# -*- coding: utf-8 -*-
import sys
import os
sys.path.append('..' + os.sep)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sh8email.settings")

import smtpd
from email.parser import Parser
from front.models import Mail
from recvmail.util import nomalize_body

import asyncore
import multiprocessing


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        body = Parser().parsestr(data)
        body = nomalize_body(body, mailfrom, peer)
        self.save_email(body)
        pass
    
    def save_email(self, body):
        m = Mail(recipient=body['to'], sender=body['from'],
                 subject=body['subject'])
        m.save()
        pass




class Sh8MailProcess(multiprocessing.Process):
    def run(self):
        self.server = CustomSMTPServer(('0.0.0.0', 25), None)
        asyncore.loop()


if __name__ == "__main__":
    p = Sh8MailProcess()
    p.start()
