# -*- coding: utf-8 -*-
import smtpd
from email.parser import Parser
from front.models import Mail

import asyncore
import multiprocessing


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        body = Parser().parsestr(data)
        self.save_email(body)
        pass
    
    def save_email(self, body):
        m = Mail(recepient=body['to'], sender=body['from'],
                 subject=body['subject'])
        m.save()


class Sh8MailProcess(multiprocessing.Process):
    def run(self):
        self.server = CustomSMTPServer(('0.0.0.0', 25), None)
        asyncore.loop()
