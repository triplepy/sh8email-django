# -*- coding: utf-8 -*-
from django.test import TestCase
import smtplib
import email.utils
from email.mime.text import MIMEText
from front.models import Mail
from .recv_server import Sh8MailProcess
import time
from .util import nomalize_recip, nomalize_body


class RecvMailTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(RecvMailTest, cls).setUpClass()
        RecvMailTest.start_mail_server(cls)
        # for wait running server
        time.sleep(0.2)
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
        time.sleep(0.2)
        mail = Mail.objects.all()
        self.assertTrue(mail)


class MailUtil(TestCase):
    def assert_after_nomalize_recipent(self, param_email, expected):
        result = nomalize_recip(param_email)
        self.assertEquals(expected, result)
    
    def test_nomalize_reciepent(self):
        self.assert_after_nomalize_recipent(
                            "recipient@example.com", "recipient")
        self.assert_after_nomalize_recipent(
                            "recip@ent@example.com", "recip@ent")
        self.assert_after_nomalize_recipent(
                            "Recipient : <recipient@example.com>", "recipient")
        self.assert_after_nomalize_recipent(
                            "Recipient : < recipient@example.com >", "recipient")

    def test_nomalize_body(self):
        p_body = {}
        p_body['from'] = "From <from@example.com>"
        p_body['to'] = "recipient@exam.com"
        p_mailfrom = ""
        p_peer = ""
        result_body = nomalize_body(p_body, p_mailfrom, p_peer)
        self.assertEquals("From <from@example.com>", result_body['from'])
        self.assertEquals("recipient", result_body['to'])

        p_mailfrom = "mailfrom@example.com"
        p_body['from'] = "From <from@example.com>"
        p_body['to'] = "recipient@exam.com"
        result_body = nomalize_body(p_body, p_mailfrom, p_peer)
        self.assertEquals("mailfrom@example.com", result_body['from'])
        self.assertEquals("recipient", result_body['to'])

        p_peer = "peer@example.com"
        p_body['from'] = "From <from@example.com>"
        p_body['to'] = "recipient@exam.com"
        result_body = nomalize_body(p_body, p_mailfrom, p_peer)
        self.assertEquals("mailfrom@example.com", result_body['from'])
        self.assertEquals("peer", result_body['to'])


class Sh8MailProcessForTest(Sh8MailProcess):
    def run(self):
        super(Sh8MailProcessForTest, self).run()

