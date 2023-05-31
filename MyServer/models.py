from django.db import models

from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings


class UserInfo(models.Model):
    USER_TYPE_CHOICES = [
        (0, '普通用户'),
        (1, 'VIP用户'),
    ]
    # username = models.CharField(verbose_name='用户名', max_length=150, unique=True)
    phone = models.CharField(verbose_name='手机号', max_length=11, unique=True, default='N/A')
    phone_code = models.CharField(verbose_name='手机验证码', max_length=4, default='N/A')
    password = models.CharField(verbose_name='密码', max_length=128)
    # token = models.CharField(verbose_name='用户TOKEN', max_length=64, null=True, blank=True)
    user_type = models.IntegerField(verbose_name='用户类型', choices=USER_TYPE_CHOICES, default=0)
    phone_code_expiry = models.DateTimeField(null=True)
    REQUIRED_FIELDS = ['password', 'user_type']
    USERNAME_FIELD = 'phone'

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def set_phone_code(self, phone_code):
        self.phone_code = phone_code
        self.phone_code_expiry = timezone.now() + timedelta(seconds=60)
        self.save()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class UserToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_auth_token', on_delete=models.CASCADE)
    token = models.CharField(max_length=40, unique=True, default='N/A')
    created = models.DateTimeField(auto_now_add=True)


class UserFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='files', on_delete=models.CASCADE)
    filename = models.CharField(max_length=40, unique=True)
