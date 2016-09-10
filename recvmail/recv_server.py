# -*- coding: utf-8 -*-
import asyncore
import multiprocessing
import smtpd
import schedule
import time

import requests
from django.conf import settings

from recvmail.msgparse import raw_to_mail, reproduce_mail


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        mail = raw_to_mail(data)
        mails = reproduce_mail(mail, rcpttos)

        for m in mails:
            # TODO 어떻게 도메인을 분리하지??
            requests.post("https://sh8.email" + "/rest/mail/", data=m)
            m.save()


class Sh8MailProcess(multiprocessing.Process):
    def run(self):
        print("SH8EMAIL SMTP SERVER IS START")
        mail_server_port = settings.MAIL_SERVER_PORT
        self.server = CustomSMTPServer(('0.0.0.0', mail_server_port), None)
        asyncore.loop()



class BatchJobSchedule(multiprocessing.Process):
    def run(self):
        def delete_job():
            # TODO 배치 잡 분리하기
            pass


        schedule.every().hour.do(delete_job)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    p = Sh8MailProcess()
    b = BatchJobSchedule()
    p.start()
    b.start()
