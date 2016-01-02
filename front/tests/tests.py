# -*- coding: utf-8 -*-
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.http.request import HttpRequest
from django.test import TestCase, Client
from django.utils import timezone
from front.checkin import MockCheckinManager
from front.models import Mail
from front.tests.utils import add_recip_to_session
from front.readauth import ReadAuthorityChecker, CannotReadReasons


class MailTest(TestCase):
    def test_delete_read(self):
        # given
        read_mail1 = self._create_mail(is_read=True)
        read_mail2 = self._create_mail(is_read=True)
        not_read_mail1 = self._create_mail(is_read=False)

        checkin_manager = MockCheckinManager(read_mail1.recipient)

        # when
        Mail.delete_read(checkin_manager)

        # then
        total_mail_count = 3
        read_mail_count = 2
        expected_mail_count = total_mail_count - read_mail_count

        self.assertEqual(Mail.objects.all().count(), expected_mail_count)

    def test_is_own(self):
        # given
        tom_mail1 = self._create_mail(recipient="Tom")
        tom_mail2 = self._create_mail(recipient="Tom")
        kitty_mail1 = self._create_mail(recipient="kitty")

        # when
        current_recipient = tom_mail1.recipient
        manager = MockCheckinManager(recipient=current_recipient)

        # then
        self.assertTrue(tom_mail1.is_own(manager))
        self.assertTrue(tom_mail2.is_own(manager))
        self.assertFalse(kitty_mail1.is_own(manager))

    def test_delete_one_day_ago(self):
        # given
        mail_today = self._create_mail()
        # create mocking mail what was created before 24 hours
        yesterday = timezone.now() - timedelta(days=1)
        mail_yesterday = self._create_mail()
        mail_yesterday.recip_date = yesterday
        mail_yesterday.save()

        # when
        Mail.delete_one_day_ago()

        # then
        self.assertEquals(1, Mail.objects.all().count())

    def test_can_read__can(self):
        recipient = 'ggone'
        secret_code = 'ssong'
        mail = Mail.objects.create(recipient=recipient, secret_code=secret_code,
                                   sender='james@google.com',
                                   subject='hello girls!',
                                   contents='Hello, nice to meet you secretly.')
        request = HttpRequest()
        request.session = {
            'recipient': recipient
        }
        request.POST['secret_code'] = secret_code

        self.assertEqual(mail.can_read(request), (True, None))

    def test_can_read__cannot(self):
        recipient = 'ggone'
        secret_code = 'ssong'
        mail = Mail.objects.create(recipient=recipient, secret_code=secret_code,
                                   sender='james@google.com',
                                   subject='hello girls!',
                                   contents='Hello, nice to meet you secretly.')
        request = HttpRequest()
        request.session = {
            'recipient': recipient
        }
        request.POST['secret_code'] = 'wrong_secret_code'

        self.assertEqual(mail.can_read(request),
                         (False, {CannotReadReasons.secret_code}))

    def _create_mail(self, recipient="recp1", sender="sender1", subject="subject1",
                     contents="contents1", is_read=False):
        return Mail.objects.create(recipient=recipient, sender=sender,
                                   subject=subject, contents=contents,
                                   is_read=is_read)


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


class ReadAuthorityCheckerTest(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.session = {
            'recipient': 'ggone'
        }
        self.secret_code = 'chinatown'

    def test_can_read(self):
        self.request.POST['secret_code'] = self.secret_code
        mail = Mail.objects.create(recipient='ggone', sender='gil@wtf.com',
                                   contents='hello sidney..',
                                   secret_code=self.secret_code)
        checker = ReadAuthorityChecker(self.request, mail)

        self.assertEqual(checker.check(), (True, None))

    def test_cannot_read__secretcode(self):
        self.request.POST['secret_code'] = 'wrong_secret_code'
        mail = Mail.objects.create(recipient='ggone', sender='gil@wtf.com',
                                   contents='hello sidney..',
                                   secret_code=self.secret_code)
        checker = ReadAuthorityChecker(self.request, mail)

        self.assertEqual(checker.check(), (False, {CannotReadReasons.secret_code}))