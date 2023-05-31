import re

from django_redis import get_redis_connection
from rest_framework.exceptions import ValidationError


def phone_validator(value):
    if not re.match(r"^(1[3|4|5|6|7|8|9])\d{9}$",value):
        raise ValidationError('手机格式错误')
def password_validator(value):
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$", value):
        raise ValidationError('密码格式错误')
def sms_code_validate(phone, code):
    if len(code) != 4:
        raise ValidationError('短信格式错误')
    if not code.isdecimal():
        raise ValidationError('短信格式错误')

    # TODO：更改为mysql
    conn = get_redis_connection()
    stored_code = conn.get(phone)
    if not stored_code:
        raise ValidationError('验证码过期')
    if code != stored_code.decode('utf-8'):
        raise ValidationError('验证码错误')