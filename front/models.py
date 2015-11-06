from django.db import models


class Mail(models.Model):
    recepient = models.CharField(max_length=50)
    sender = models.CharField(max_length=200)
    subject = models.CharField(max_length=400)
    contents = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
