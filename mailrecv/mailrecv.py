# -*- coding: utf-8 -*-

import smtpd
from email.parser import Parser
import asyncore

from front.models import Mail


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))



        body = Parser().parsestr(data)
        Mail(recepient=body['to'], sender=body['from'], subject=body['subject'])

        return

server = CustomSMTPServer(('localhost', 25), None)

asyncore.loop()
