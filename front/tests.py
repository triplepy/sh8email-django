# -*- coding: utf-8 -*-
from django.test import TestCase
from datetime import timedelta
from django.utils import timezone
from .models import Mail


class BatchTest(TestCase):

    def setUp(self):
        # create mocking mail what was created before 24 hours
        yesterday = timezone.now() - timedelta(days=1)

        Mail.objects.create(
            recipient="test_delete_mail_util",
            sender="delete_mail_sender",
            subject="This will be deleted",
            contents="코오오ㅇ온텐트",
        )
        
        Mail.objects.filter(pk=1).update(recip_date=yesterday)
        
        Mail.objects.create(
            recipient="test_delete_mail_util",
            sender="delete_mail_sender",
            subject="This will be deleted",
            contents="코오오ㅇ온텐트",
        )

    def test_delete_mail_util(self):
        # call delete_mail_util method
        Mail.delete_one_day_ago(Mail)
        # check mail
        mails = Mail.objects.all()
        self.assertEquals(1, Mail.objects.count())
