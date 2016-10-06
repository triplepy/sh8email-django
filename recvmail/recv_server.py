# -*- coding: utf-8 -*-
import asyncore
import logging
import multiprocessing
import smtpd

from django.conf import settings

from recvmail.msgparse import raw_to_mail, reproduce_mail

logger = logging.getLogger(__name__)


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        try:
            mail = raw_to_mail(data)
            mails = reproduce_mail(mail, rcpttos)

            for m in mails:
                m.save()
        except BaseException as e:
            logger.exception("Exception raised in CustomSMTPServer#process_message()")
            raise


class Sh8MailProcess(multiprocessing.Process):
    def run(self):
        mail_server_port = settings.MAIL_SERVER_PORT
        CustomSMTPServer(('0.0.0.0', mail_server_port), None)
        asyncore.loop()
