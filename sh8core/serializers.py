from rest_framework import serializers
from sh8core.models import Mail


class MailSerializer(serializers.Serializer):
    recipient = serializers.CharField(max_length=50)
    secret_code = serializers.CharField(max_length=16)
    sender = serializers.CharField(max_length=200)
    subject = serializers.CharField(max_length=400)
    contents = serializers.CharField()
    recip_date = serializers.DateTimeField()
    is_read = serializers.BooleanField(default=False)



