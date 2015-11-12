# -*- coding: utf-8 -*-
from django.test import TestCase
import smtplib
import email.utils
from email.mime.text import MIMEText
from front.models import Mail
from .recv_server import Sh8MailProcess
import time
from .util import nomalize_recip


class RecvMailTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(RecvMailTest, cls).setUpClass()
        RecvMailTest.start_mail_server(cls)
        # for wait running server
        time.sleep(0.5)
        RecvMailTest.send_test_mail(cls)

    def send_test_mail(self):
        # Create the message
        msg = MIMEText('This is the body of the message.')
        msg['To'] = email.utils.formataddr(('Recipient',
                                            'recipient@example.com'))
        msg['From'] = email.utils.formataddr(('Author', 'author@example.com'))
        msg['Subject'] = 'Simple test message'

        server = smtplib.SMTP('127.0.0.1', 25)
        # show communication with the server
        try:
            server.sendmail('author@example.com',
                            ['recipient@example.com'],
                            msg.as_string())
        finally:
            server.quit()

    def start_mail_server(self):
        p = Sh8MailProcessForTest()
        p.daemon = True
        p.start()

    def test_exist_a_mail(self):
        time.sleep(1)
        mail = Mail.objects.all()
        self.assertTrue(mail)


class MailUtil(TestCase):
    def test_nomalize_reciepent(self):
        param_email = "recpient@example.com"
        result = nomalize_recip(param_email)
        self.assertEquals("recpient", result)

        param_email = "recip@ent@example.com"
        result = nomalize_recip(param_email)
        self.assertEquals("recip@ent", result)

    
class Sh8MailProcessForTest(Sh8MailProcess):
    def run(self):
        super(Sh8MailProcessForTest, self).run()

