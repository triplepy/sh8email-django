from datetime import datetime
from django.db import models


class Mail(models.Model):
    recipient = models.CharField(max_length=50)
    sender = models.CharField(max_length=200)
    subject = models.CharField(max_length=400)
    contents = models.TextField()
    recip_date = models.DateTimeField(auto_now_add=True)

    def delete_one_day_ago(self):
        yesterday = datetime.now() - timedelta(days=1)
        mail_to_delete = self.objects.filter(recip_date__lte=(date))
        mail_to_delete.delete()

