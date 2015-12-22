# -*- coding: utf-8 -*-
from django.test import TestCase
from datetime import timedelta
from django.utils import timezone
from front.checkin import MockCheckinManager

from .models import Mail

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

    def _create_mail(self, recipient="recp1", sender="sender1", subject="subject1",
                     contents="contents1", is_read=False):
        return Mail.objects.create(recipient=recipient, sender=sender, subject=subject,
                                   contents=contents, is_read=is_read)

class DetailViewTest(TestCase):
    # TODO should make tests.
    def test_secret_code_check(self):
        # 암호가 걸린 메일을 클릭했다. 암호 입력창이 뜬다.
        # 암호를 입력한 뒤에 메일이 보인다.
        mail = Mail.objects.create(recipient="recp11", secret_code="code11", sender="sender11", subject="subject11", contents="contents11")
        correct_code = "code11"
        wrong_code = "code22"
        is_valid = Mail.check_secret_code(mail, correct_code)
        is_not_valid = Mail.check_secret_code(mail, wrong_code)
        self.assertTrue(is_valid)
        self.assertFalse(is_not_valid)
