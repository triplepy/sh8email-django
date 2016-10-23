# -*- coding: utf-8 -*-
import asyncore
import logging
import multiprocessing
import os
import smtpd
import uuid

from django.conf import settings

from recvmail.msgparse import raw_to_mail, reproduce_mail

logger = logging.getLogger(__name__)


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        rcpttos_filtered = [r for r in rcpttos if '@sh8.email' in r]
        if len(rcpttos_filtered) == 0: return
        
        # TODO Redesign this logic, and write tests code of exception logic.
        try:
            mail = raw_to_mail(data)
            mails = reproduce_mail(mail, rcpttos_filtered)

            for m in mails:
                m.save()
        except BaseException as e:
            dir_path = os.path.join(settings.BASE_DIR, "log/raw_messages/")
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
            file_name = "{}.msg".format(str(uuid.uuid4()))
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'w') as f:
                f.write(data)
            logger.exception("""\
{}
Parameter info below.
[peer]
{}
[mailfrom]
{}
[rcpttos]
{}
[data]
{}
[**kwargs]
{}""".format(str(e), peer, mailfrom, rcpttos, "'data' is recorded to file located in '{}'".format(file_path), kwargs))
            raise


class Sh8MailProcess(multiprocessing.Process):
    def run(self):
        mail_server_port = settings.MAIL_SERVER_PORT
        CustomSMTPServer(('0.0.0.0', mail_server_port), None)
        asyncore.loop()
