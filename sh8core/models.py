from datetime import timedelta

from django.db import models
from django.utils import timezone

from sh8core.readauth import ReadAuthorityChecker


class Mail(models.Model):
    recipient = models.CharField(max_length=50, db_index=True)
    # TODO change default null -> blank
    secret_code = models.CharField(max_length=16, null=True, blank=True)
    sender = models.CharField(max_length=200)
    subject = models.CharField(max_length=400)
    contents = models.TextField()
    recip_date = models.DateTimeField(auto_now_add=True, editable=True)
    is_read = models.BooleanField(default=False)

    @classmethod
    def delete_read(cls, checkin_manager):
        to_delete = cls.objects.filter(
            is_read=True, recipient=checkin_manager.current_recipient())
        to_delete.delete()

    @classmethod
    def delete_one_day_ago(cls):
        yesterday = timezone.now() - timedelta(days=1)
        to_delete = cls.objects.filter(recip_date__lte=yesterday)
        to_delete.delete()

    def is_own(self, checkin_manager):
        return checkin_manager.current_recipient() == self.recipient

    def read(self):
        self.is_read = True
        self.save()

    def can_read(self, request):
        checker = ReadAuthorityChecker(request, self)
        return checker.check()

    def is_secret(self):
        return bool(self.secret_code)

    def __repr__(self):
        return "Mail(recipient={}, secret_code={}, sender={}, subject={}, contents={}, recip_date={}, is_read={})".format(
            self.recipient, self.secret_code, self.sender, self.subject, self.contents, self.recip_date, self.is_read)

    def __str__(self):
        return self.__repr__()
