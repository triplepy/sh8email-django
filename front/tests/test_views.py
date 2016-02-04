from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.test import TestCase, Client
from front.models import Mail
from front.tests.utils import add_recip_to_session


class IntroViewTest(TestCase):
    def test_page_visible(self):
        client = Client()
        response = client.get(reverse('front:intro'))
        self.assertContains(response, '쉿 메일?')


class DetailViewTest(TestCase):
    def setUp(self):
        self.recipient = 'ggone'
        self.client = Client()
        self.mail = Mail.objects.create(recipient=self.recipient, sender='sender1',
                                        subject='subject1', contents='contents1')

    def test_simplest_success_case(self):
        add_recip_to_session(self.client, self.recipient)
        self.response = self.client.get(
                reverse('front:detail', args=(self.mail.pk,)))

        self.assertContains(self.response, self.mail.subject)

    def test_not_checkin(self):
        self.response = self.client.get(
                reverse('front:detail', args=(self.mail.pk,)))
        self.assertEqual(self.response.status_code,
                         HttpResponseForbidden.status_code)

    def test_checkin_other_recipient(self):
        checkin_recipient = 'wonyoung'
        add_recip_to_session(self.client, checkin_recipient)

        self.response = self.client.get(
                reverse('front:detail', args=(self.mail.pk,)))

        self.assertEqual(self.response.status_code,
                         HttpResponseForbidden.status_code)

    def test_not_exists_mail(self):
        notexistsmail_pk = self.mail.pk
        # After now, the mail isn't exists.
        self.mail.delete()

        add_recip_to_session(self.client, self.recipient)

        self.response = self.client.get(
                reverse('front:detail', args=(notexistsmail_pk,)))

        self.assertEqual(self.response.status_code, 404)


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
        response = client.post(reverse('front:detail', args=(mail.pk,)),
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
        response = client.post(reverse('front:detail', args=(mail.pk,)),
                               data={'secret_code': 'wrong_secretcode'})

        # then
        self.assertTemplateUsed(response, 'front/secretcode_form.html')