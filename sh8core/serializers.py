from rest_framework import serializers


class MailListSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    recipient = serializers.CharField(max_length=50)
    sender = serializers.CharField(max_length=200)
    subject = serializers.CharField(max_length=400)
    contents = serializers.CharField(max_length=30)
    recip_date = serializers.DateTimeField()
    isSecret = serializers.BooleanField(source='is_secret')
    is_read = serializers.BooleanField(default=False)


class MailDetailSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    recipient = serializers.CharField(max_length=50)
    sender = serializers.CharField(max_length=200)
    subject = serializers.CharField(max_length=400)
    contents = serializers.CharField()
    recip_date = serializers.DateTimeField()
    is_read = serializers.BooleanField(default=False)
