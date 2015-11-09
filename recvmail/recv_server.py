# -*- coding: utf-8 -*-
import smtpd
from email.parser import Parser
from front.models import Mail
from django.db import connection
import threading
import asyncore
import multiprocessing


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        
        body = Parser().parsestr(data)
        print("-----------------------")
        m = Mail(recepient=body['to'], sender=body['from'],
                 subject=body['subject'])
        print("++++++++++++++++++++++++++")
        m.save()
        print("++++++++++++++++++++++++++")
        mail = Mail.objects.all()
        print("-----------------------")
        print(mail[0].subject)
        print("================= \n ", body['to'])
        print("=================")
        return


class Sh8MailProcess(multiprocessing.Process):
    def run(self):
        self.server = CustomSMTPServer(('0.0.0.0', 25), None)
        asyncore.loop()

        
class Sh8MailThread(object):
    def start(self):
        self.smtp = CustomSMTPServer(('0.0.0.0', 25), None)
        # time out parameter is important,
        # otherwise code will block 30 seconds after smtp has been close
        self.thread = threading.Thread(target=asyncore.loop,
                                       kwargs={'timeout': 1})

    def stop(self):
        self.smtp.close()
        # now it is save to wait for the thread to finish,
        # i.e. for asyncore.loop() to exit
        self.thread.join()
