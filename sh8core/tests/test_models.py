# -*- coding: utf-8 -*-
from datetime import timedelta

from django.http.request import HttpRequest
from django.test import TestCase
from django.utils import timezone

from sh8core.checkin import MockCheckinManager
from sh8core.models import Mail
from sh8core.readauth import CannotReadReasons


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

        self.assertEqual(expected_mail_count, Mail.objects.all().count())

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

        self.assertEqual((True, None), mail.can_read(request))

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

        self.assertEqual((False, {CannotReadReasons.secret_code}),
                         mail.can_read(request))

    def _create_mail(self, recipient="recp1", sender="sender1", subject="subject1",
                     contents="contents1", is_read=False):
        return Mail.objects.create(recipient=recipient, sender=sender,
                                   subject=subject, contents=contents,
                                   is_read=is_read)
