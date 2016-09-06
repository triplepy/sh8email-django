import requests

from django.test import LiveServerTestCase

from sh8core.models import Mail


class MailReceiveTest(LiveServerTestCase):
    def test_mail_received(self):
        mail_data = {
            "recipient": "test_mail_received",
            "sender": "sender@sh8.email",
            "subject": "test_mail_received subject",
            "contents": "contconctonctonctonctoncton$$$$$$$$!@#@!%!^#$%^$%^&^&%(("
        }

        requests.post(url=self.live_server_url + "/rest/mail/", data=mail_data)
        mail = Mail.objects.get(recipient=mail_data["recipient"])

        self.assertTrue(mail)
        self.assertEqual(mail.sender, mail_data["sender"])
        self.assertEqual(mail.subject, mail_data["subject"])
        self.assertEqual(mail.contents, mail_data["contents"])