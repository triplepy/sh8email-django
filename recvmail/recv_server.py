# -*- coding: utf-8 -*-
import asyncore
import multiprocessing
import smtpd
import schedule
import time

from django.conf import settings

from recvmail.msgparse import raw_to_mail, reproduce_mail
from sh8core.models import Mail


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


class MailDeleteBatch(multiprocessing.Process):
    def run(self):
        def delete_job():
            Mail.delete_one_day_ago()

        schedule.every().hour.do(delete_job)

        while True:
            schedule.run_pending()
            time.sleep(1)