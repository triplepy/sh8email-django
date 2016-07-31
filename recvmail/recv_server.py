# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sh8email.settings")

from recvmail.msgparse import raw_to_mail, reproduce_mail

import asyncore
import multiprocessing
import smtpd
import schedule
import time

import django
from django.conf import settings

from front.models import Mail


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        mail = raw_to_mail(data)
        mails = reproduce_mail(mail, rcpttos)

        for m in mails:
            m.save()


class Sh8MailProcess(multiprocessing.Process):
    def run(self):
        self.server = CustomSMTPServer(('0.0.0.0', settings.MAIL_SERVER_PORT), None)
        asyncore.loop()


class BatchJobSchedule(multiprocessing.Process):
    def run(self):
        def delete_job():
            django.setup()
            return Mail.delete_one_day_ago()

        schedule.every().hour.do(delete_job)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    p = Sh8MailProcess()
    b = BatchJobSchedule()
    p.start()
    b.start()
