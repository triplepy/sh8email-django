from django.test import TestCase
import smtplib
import email.utils
from email.mime.text import MIMEText
from front.models import Mail
from recvmail.recv_server import Sh8MailThread
import threading

t = Sh8MailThread()


def server_start():
    t.start()


t_start = threading.Thread(target=server_start())


class RecvMailTest(TestCase):

    def setUp(self):
        t_start.start()
        # Create the message
        msg = MIMEText('This is the body of the message.')
        msg['To'] = email.utils.formataddr(('Recipient',
                                            'recipient@example.com'))
        msg['From'] = email.utils.formataddr(('Author', 'author@example.com'))
        msg['Subject'] = 'Simple test message'

        server = smtplib.SMTP('127.0.0.1', 25)
        # show communication with the server
        server.set_debuglevel(True) 
        try:
            server.sendmail('author@example.com',
                            ['recipient@example.com'],
                            msg.as_string())
        finally:
            server.quit()
        
    def tearDown(self):
        t.stop()

    def test_get_a_mail(self):
        mail = Mail.objects.all()
        self.assertTrue(mail)

