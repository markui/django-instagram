from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


# 다른 형태의 json을 보여주고 싶음 -> 따라서 2개를 분리함
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password',
            'img_profile',
        )


class SignupSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'img_profile',
            'password1',
            'password2',
            'token',
        )

    def validate(self, data):
        """
        password1, password2가 일치하는지 확인
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다")
        return data

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            img_profile=validated_data['img_profile'],
        )
    # read, 즉 serialize를 할 경우에만 사용되는 SerializerMethodField
    # obj: serializer.save()로 만들어진 user instance가 온다
    def get_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key

