from django.test import TestCase
import smtplib
import email.utils
from email.mime.text import MIMEText
from front.models import Mail
from .recv_server import Sh8MailProcess
import time


class RecvMailTest(TestCase):

    def setUp(self):
        self.p = Sh8MailProcessForTest()
        self.p.daemon = True
        self.p.start()
        time.sleep(0.5)
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
            
    def test_get_a_mail(self):
        time.sleep(10)
        mail = Mail.objects.all()

        self.assertTrue(mail)


class Sh8MailProcessForTest(Sh8MailProcess):
    def run(self):
        super(Sh8MailProcessForTest, self).run()

