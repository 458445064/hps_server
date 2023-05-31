from rest_framework.authentication import BaseAuthentication
from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
import datetime
import pytz
from MyServer import models
from rest_framework.permissions import BasePermission


class LoginAuth(BaseAuthentication):
    def authenticate(self, request):
        '''
        1 对token设置14天有效时间
        2 缓存存储
        :param request:
        :return:
        '''
        # print(request.META.get("HTTP_AUTHORIZATION"))
        token=request.META.get("HTTP_AUTHORIZATION")
        # 1 校验是否存在token字符串
        # 1.1 缓存校验
        user=cache.get(token)
        if user:
            print("缓存校验成功")
            return user,token
        # 1.2 数据库校验
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise AuthenticationFailed("认证失败！")

        # 2 校验是否在有效期内
        print(token_obj.created)    # 2018-1-1- 0 0 0
        now=datetime.datetime.now() # 2018-1-12- 0 0 0
        now = now.replace(tzinfo=pytz.timezone('UTC'))
        print(now-token_obj.created)
        delta=now - token_obj.created
        state=delta < datetime.timedelta(weeks=1)
        print(state)
        if state:
            # 校验成功，写入缓存中
            print("delta",delta)
            delta=datetime.timedelta(weeks=2)-delta
            print(delta.total_seconds())
            cache.set(token_obj.token,token_obj.user,min(delta.total_seconds(),3600*24*7))
            print("数据库校验成功")
            return token_obj.user,token_obj.token
        else:
            raise  AuthenticationFailed("认证超时！")


class IsVipUser(BasePermission):
    def has_permission(self, request, view):
        # 检查用户的 user_type 是否是 1 (即VIP用户)
        if request.user and request.user.user_type == 1:
            return True
        else:
            raise PermissionDenied("不是vip用户！")