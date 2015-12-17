from datetime import datetime, timedelta, MINYEAR
from django.utils import timezone
from django.db import models
from .checkin import current_recipient


class Mail(models.Model):
    recipient = models.CharField(max_length=50)
    sender = models.CharField(max_length=200)
    subject = models.CharField(max_length=400)
    contents = models.TextField()
    recip_date = models.DateTimeField(auto_now_add=True, editable=True)
    is_read = models.BooleanField(default=False)

    @classmethod
    def delete_read(cls, request):
        print(current_recipient(request))
        to_delete = cls.objects.filter(
                is_read=True, recipient=current_recipient(request))
        print(to_delete)
        to_delete.delete()

    def is_own(self, request):
        return current_recipient(request) == self.recipient

    def delete_one_day_ago(self):
        # for delete batch job
        yesterday = timezone.now() - timedelta(days=1)
        to_delete = self.objects.filter(
                recip_date__lte=yesterday)
        to_delete.delete()
