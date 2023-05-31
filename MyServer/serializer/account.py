from datetime import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from MyServer import models
from .validators import phone_validator, password_validator


def validate_sms_code(phone, code):
    user_info = models.UserInfo.objects.get(phone=phone)
    value = code
    if value != user_info.phone_code:
        raise serializers.ValidationError('短信验证码错误')
    if timezone.now() > user_info.phone_code_expiry:
        raise serializers.ValidationError('短信验证码过期')


class MessageSerializer(serializers.Serializer):
    phone = serializers.CharField(label='手机号', validators=[phone_validator, ])
    image_code = serializers.CharField(label='图片验证码')

    def validated_image_code(self, value):
        session_code = self.context['request'].session.get('image_code')
        # 比较 session 中的验证码和用户提交的验证码
        if value != session_code:
            raise serializers.ValidationError('图片验证码错误')

        return value


class RegisterSerializer(serializers.Serializer):
    # username = serializers.CharField(label='用户名', max_length=150, min_length=6)
    phone = serializers.CharField(label='手机号', validators=[phone_validator, ])
    agreement = serializers.BooleanField(label='协议', default=False)
    password = serializers.CharField(label='密码', validators=[password_validator, ], max_length=128, min_length=8)
    image_code = serializers.CharField(label='图片验证码')
    confirm_password = serializers.CharField(label='确认密码', max_length=128, min_length=8)
    code = serializers.CharField(label='短信验证码')

    def validate_agreement(self, value):
        if not value:
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate_image_code(self, value):

        session_code = self.context['request'].session.get('image_code')
        # 比较 session 中的验证码和用户提交的验证码
        if value != session_code:
            raise serializers.ValidationError('图片验证码错误')

        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("两次密码不一致")
        return data

    def validate_code(self, value):
        phone = self.initial_data.get('phone')
        validate_sms_code(phone, value)

        return value

    def create(self, validated_data):
        # 删除多余字段
        del validated_data['confirm_password']
        del validated_data['image_code']
        del validated_data['code']
        # 创建用户
        user = super().create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(label='手机号', validators=[phone_validator, ])
    password = serializers.CharField(label='密码', max_length=128, min_length=8)
    agreement = serializers.BooleanField(label='协议', default=False)
    image_code = serializers.CharField(label='图片验证码')
    phone_code = serializers.CharField(label='短信验证码', required=False)
    password = serializers.CharField(label='密码', required=False)
    login_method = serializers.ChoiceField(choices=['sms', 'password'])

    def validate_agreement(self, value):
        if not value:
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validated_image_code(self, value):

        session_code = self.context['request'].session.get('image_code')
        # 比较 session 中的验证码和用户提交的验证码
        if value != session_code:
            raise serializers.ValidationError('图片验证码错误')
        return value

    def validate(self, data):
        login_method = data.get('login_method')
        if login_method == 'sms':
            # 使用短信验证码登录，验证短信验证码
            user_info = models.UserInfo.objects.get(phone=self.initial_data['phone'])
            value = data.get('phone_code')
            if value != user_info.phone_code:
                raise serializers.ValidationError('短信验证码错误')
            if timezone.now() > user_info.phone_code_expiry:
                raise serializers.ValidationError('短信验证码过期')
        elif login_method == 'password':
            # 使用密码登录，验证密码
            password = data.get('password')
            user = models.UserInfo.objects.get(phone=data.get('phone'))
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误')
        else:
            raise serializers.ValidationError('登录方式错误')
        return data
