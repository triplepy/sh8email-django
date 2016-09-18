from rest_framework import serializers


class MailListSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    pk = serializers.IntegerField(read_only=True)
    recipient = serializers.CharField(max_length=50)
    sender = serializers.CharField(max_length=200)
    subject = serializers.CharField(max_length=400)
    contents = serializers.CharField(max_length=30)
    recipDate = serializers.DateTimeField(source='recip_date')
    isSecret = serializers.BooleanField(source='is_secret')
    isRead = serializers.BooleanField(default=False, source='is_read')


class MailDetailSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    pk = serializers.IntegerField(read_only=True)
    recipient = serializers.CharField(max_length=50)
    sender = serializers.CharField(max_length=200)
    subject = serializers.CharField(max_length=400)
    contents = serializers.CharField()
    recipDate = serializers.DateTimeField(source='recip_date')
    isRead = serializers.BooleanField(default=False, source="is_read")
