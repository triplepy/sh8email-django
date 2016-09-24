from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.test import TestCase, Client

from sh8core.models import Mail
from sh8core.tests.utils import add_recip_to_session


class IntroViewTest(TestCase):
    def test_page_visible(self):
        client = Client()
        response = client.get(reverse('web:intro'))
        self.assertContains(response, '세상에서 가장 조용한 이메일')


class ListViewTest(TestCase):
    def test_list_is_shown(self):
        self.mail1 = Mail.objects.create(recipient='ggone', sender='hagyoon@gmail.com',
                                         subject='subject1', contents='contents1')
        self.mail2 = Mail.objects.create(recipient='ggone', sender='silver@gmail.com',
                                         subject='subject2', contents='contents2')
        mails = [self.mail1, self.mail2]

        client = Client()
        add_recip_to_session(client, 'ggone')
        response = client.get(reverse('web:list'))

        for mail in mails:
            self.assertContains(response, mail.sender)
            self.assertContains(response, mail.subject[:50])
            self.assertContains(response, mail.contents[:200])

    def test_content_of_secretmail_should_not_be_shown(self):
        self.mail1 = Mail.objects.create(recipient='ggone', sender='hagyoon@gmail.com',
                                         subject='subject3', contents='contents3', secret_code='secret')
        self.mail2 = Mail.objects.create(recipient='ggone', sender='silver@gmail.com',
                                         subject='subject4', contents='contents4', secret_code='secret')

        mails = [self.mail1, self.mail2]

        client = Client()
        add_recip_to_session(client, 'ggone')
        response = client.get(reverse('web:list'))

        for mail in mails:
            self.assertTrue(mail.is_secret())
            self.assertContains(response, mail.sender)
            self.assertContains(response, mail.subject[:50])
            self.assertNotContains(response, mail.contents[:200])


class DetailViewTest(TestCase):
    def setUp(self):
        self.recipient = 'ggone'
        self.client = Client()
        self.mail = Mail.objects.create(recipient=self.recipient, sender='sender1',
                                        subject='subject1', contents='contents1')

    def test_simplest_success_case(self):
        add_recip_to_session(self.client, self.recipient)
        self.response = self.client.get(
            reverse('web:detail', args=(self.mail.pk,)))

        self.assertContains(self.response, self.mail.subject)

    def test_not_checkin(self):
        self.response = self.client.get(
            reverse('web:detail', args=(self.mail.pk,)))
        self.assertEqual(self.response.status_code,
                         HttpResponseForbidden.status_code)

    def test_checkin_other_recipient(self):
        checkin_recipient = 'wonyoung'
        add_recip_to_session(self.client, checkin_recipient)

        self.response = self.client.get(
            reverse('web:detail', args=(self.mail.pk,)))

        self.assertEqual(self.response.status_code,
                         HttpResponseForbidden.status_code)

    def test_not_exists_mail(self):
        notexistsmail_pk = self.mail.pk
        # After now, the mail isn't exists.
        self.mail.delete()

        add_recip_to_session(self.client, self.recipient)

        self.response = self.client.get(
            reverse('web:detail', args=(notexistsmail_pk,)))

        self.assertEqual(self.response.status_code, 404)

    def test_html_sanitized_striphtml(self):
        # given
        client = Client()
        recipient = 'ggone'
        original_html = '''
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width">
</head>
<body yahoo='fix' style='margin-top:0;margin-bottom:0;margin-left:0;margin-right:0;'>
  <img src="https://www.amazon.com/gp/0.jpg">
  <img src="https://www.amazon.com/gp/1.jpg" onerror="alert('shit!')">
  <script>alert('shit!')</script>
</body>
</html>
'''
        # when
        mail = Mail.objects.create(recipient=recipient, sender='jong@google.com',
                                   subject='secret mail.', contents=original_html)
        add_recip_to_session(client, recipient)
        response = client.get(reverse('web:detail', args=(mail.pk,)))

        # then
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<img src=\"https://www.amazon.com/gp/0.jpg\">",
                            msg_prefix="Response was " + str(response.content))
        self.assertContains(response, "alert&#40;'shit!'&#41;", msg_prefix="Response was " + str(response.content))
        self.assertNotContains(response, "onerror=\"alert('shit!')\"",
                               msg_prefix="Response was " + str(response.content))
        self.assertNotContains(response, "<script>alert('shit!')</script>",
                               msg_prefix="Response was " + str(response.content))


class DetailViewWithSecretcodeTest(TestCase):
    def test_success_case(self):
        # given
        client = Client()
        recipient = 'ggone'
        secret_code = 'christmas_dream'

        # when
        mail = Mail.objects.create(recipient=recipient, sender='jong@google.com',
                                   subject='secret mail.', contents='iloveyou',
                                   secret_code=secret_code)
        add_recip_to_session(client, recipient)
        response = client.post(reverse('web:detail', args=(mail.pk,)),
                               data={'secret_code': secret_code})

        # then
        self.assertContains(response, mail.contents)

    def test_secretcode_notmatch(self):
        # given
        client = Client()
        recipient = 'ggone'
        secret_code = 'christmas_dream'

        # when
        mail = Mail.objects.create(recipient=recipient, sender='jong@google.com',
                                   subject='secret mail.', contents='iloveyou',
                                   secret_code=secret_code)
        add_recip_to_session(client, recipient)
        response = client.post(reverse('web:detail', args=(mail.pk,)),
                               data={'secret_code': 'wrong_secretcode'})

        # then
        self.assertTemplateUsed(response, 'web/secretcode_form.html')
