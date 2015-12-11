from datetime import datetime, timedelta, MINYEAR
from django.utils import timezone
from django.db import models


class Mail(models.Model):
    recipient = models.CharField(max_length=50)
    sender = models.CharField(max_length=200)
    subject = models.CharField(max_length=400)
    contents = models.TextField()
    recip_date = models.DateTimeField(auto_now_add=True, editable=True)

    def delete_one_day_ago(self):
        yesterday = timezone.now() - timedelta(days=1)
        mail_to_delete = self.objects.filter(
            recip_date__lte=yesterday)
        print(mail_to_delete)
        mails = Mail.objects.all()
        print("==============", mails[0].recip_date)
        print("==============", mails[1].recip_date)
        mail_to_delete.delete()

