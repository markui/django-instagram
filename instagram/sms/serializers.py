from rest_framework import serializers

from .validators import phone_number, sms_length


# 안에 validators는 data를 return할 수 없고 검증 과정만 한다.
class SMSSerializer(serializers.Serializer):
    receiver = serializers.CharField(
        validators=[phone_number]
    )
    message = serializers.CharField(
        validators=[sms_length]
    )

    def validate_receiver(self, value):
        return value.replace('-', '')
