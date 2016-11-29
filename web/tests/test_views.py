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
    fixtures = ['web/mails.yaml']

    def test_list_is_shown_when_plain_mail(self):
        plain_mail1 = Mail.objects.get(pk=1)
        plain_mail2 = Mail.objects.get(pk=2)
        mails = [plain_mail1, plain_mail2]

        client = Client()
        add_recip_to_session(client, plain_mail1.recipient)
        response = client.get(reverse('web:list'))

        for mail in mails:
            self.assertContains(response, mail.sender)
            self.assertContains(response, mail.subject[:50])
            self.assertContains(response, mail.contents[:200])

    def test_list_should_not_be_shown_when_html_mail(self):
        html_mail1 = Mail.objects.get(pk=5)
        html_mail2 = Mail.objects.get(pk=6)
        mails = [html_mail1, html_mail2]

        client = Client()
        add_recip_to_session(client, html_mail1.recipient)
        response = client.get(reverse('web:list'))

        for mail in mails:
            self.assertContains(response, mail.sender)
            self.assertContains(response, mail.subject[:50])
            self.assertNotContains(response, mail.contents[:200])

    def test_content_of_secretmail_should_not_be_shown(self):
        mail1 = Mail.objects.get(pk=3)
        mail2 = Mail.objects.get(pk=4)

        mails = [mail1, mail2]

        client = Client()
        add_recip_to_session(client, 'ggone')
        response = client.get(reverse('web:list'))

        for mail in mails:
            self.assertTrue(mail.is_secret())
            self.assertContains(response, mail.sender)
            self.assertContains(response, mail.subject[:50])
            self.assertNotContains(response, mail.contents[:200])


class DetailViewTest(TestCase):
    fixtures = ['web/mails.yaml']

    def setUp(self):
        self.client = Client()
        self.mail = Mail.objects.get(pk=1)
        self.recipient = self.mail.recipient

    def test_simplest_success_case(self):
        add_recip_to_session(self.client, self.recipient)
        self.response = self.client.get(
            reverse('web:detail', args=(self.mail.pk,)))

        self.assertContains(self.response, self.mail.subject)

    def test_not_checkin(self):
        self.response = self.client.get(
            reverse('web:detail', args=(self.mail.pk,)))
        self.assertEqual(HttpResponseForbidden.status_code,
                         self.response.status_code)

    def test_checkin_other_recipient(self):
        checkin_recipient = "I am not" + self.recipient
        add_recip_to_session(self.client, checkin_recipient)

        self.response = self.client.get(
            reverse('web:detail', args=(self.mail.pk,)))

        self.assertEqual(HttpResponseForbidden.status_code,
                         self.response.status_code)

    def test_not_exists_mail(self):
        notexistsmail_pk = self.mail.pk
        # After now, the mail isn't exists.
        self.mail.delete()

        add_recip_to_session(self.client, self.recipient)

        self.response = self.client.get(
            reverse('web:detail', args=(notexistsmail_pk,)))

        self.assertEqual(404, self.response.status_code)

    def test_html_sanitized_clean_html(self):
        # given
        client = Client()
        # when
        mail = Mail.objects.get(pk=5)
        add_recip_to_session(client, mail.recipient)
        response = client.get(reverse('web:detail', args=(mail.pk,)))

        # then
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "<img src=\"https://www.amazon.com/gp/0.jpg\">",
                            msg_prefix="Response was " + str(response.content))
        self.assertNotContains(response, "onerror=\"alert('shit!')\"",
                               msg_prefix="Response was " + str(response.content))
        self.assertNotContains(response, "<script>alert('shit!')</script>",
                               msg_prefix="Response was " + str(response.content))
        self.assertContains(response, "margin-top:0;margin-bottom:0;margin-left:0;margin-right:0;",
                               msg_prefix="Response was " + str(response.content))


class DetailViewWithSecretcodeTest(TestCase):
    fixtures = ['web/mails.yaml']

    def test_success_case(self):
        # given
        client = Client()

        # when
        mail = Mail.objects.get(pk=3)
        add_recip_to_session(client, mail.recipient)
        response = client.post(reverse('web:detail', args=(mail.pk,)),
                               data={'secret_code': mail.secret_code})

        # then
        self.assertContains(response, mail.contents)

    def test_secretcode_notmatch(self):
        # given
        client = Client()

        # when
        mail = Mail.objects.get(pk=3)
        add_recip_to_session(client, mail.recipient)
        response = client.post(reverse('web:detail', args=(mail.pk,)),
                               data={'secret_code': 'wrong_secretcode'})

        # then
        self.assertTemplateUsed(response, 'web/secretcode_form.html')
