# -*- coding: utf-8 -*-
import asyncore
import multiprocessing
import smtpd

from django.conf import settings

from recvmail.msgparse import raw_to_mail, reproduce_mail


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        mail = raw_to_mail(data)
        mails = reproduce_mail(mail, rcpttos)

        for m in mails:
            m.save()


class Sh8MailProcess(multiprocessing.Process):
    def run(self):
        mail_server_port = settings.MAIL_SERVER_PORT
        self.server = CustomSMTPServer(('0.0.0.0', mail_server_port), None)
        asyncore.loop()


