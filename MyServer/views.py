import oss2
import random
import uuid

from django.utils import timezone
from django.core.cache import cache

from utils.auth import LoginAuth
from utils.imagecode import check_code
from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection
from django.http import HttpResponse
from MyServer import models
from utils.sms.msg import send_message
from MyServer.serializer.account import MessageSerializer, LoginSerializer, RegisterSerializer

from ServerTest.settings import ALIBABA_OSS_ACCESS_KEY_ID, ALIBABA_OSS_ACCESS_KEY_SECRET, ALIBABA_BUCKET_ENDPOINT, ALIBABA_SECURITYTOKEN,ALIBABA_OSS_BUCKET_NAME
class MessageView(APIView):
    def get(self, request, *args, **kwargs):
        """
        发送手机短信验证码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 1.获取手机号
        # 2.手机格式校验
        print(request.query_params)
        ser = MessageSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'status': False,'errors': ser.errors})
        phone = ser.validated_data.get('phone')

        # 3.生成随机验证码
        random_code = random.randint(1000, 9999)
        # 5.把验证码+手机号保留（30s过期）

        result = send_message(phone,random_code)
        if not result:
            return Response({"status": False, 'message': '短信发送失败'})

        print(random_code)
        conn = get_redis_connection()
        conn.set(phone, random_code, ex=60)

        return Response({"status": True})

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": False, 'message': '注册失败', 'errors': serializer.errors})
        serializer.save()

        return Response({"status": True})

class LoginView(APIView):
    authentication_classes = [LoginAuth]
    def post(self, request, *args, **kwargs):
        if request.user:
            return Response({"status": True, "data": {"token": request.auth, 'phone': request.user.phone}})
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False, 'message': '登录失败', 'errors': ser.errors})

        # 3. 去数据库中获取用户信息（获取/创建）
        phone = ser.validated_data.get('phone')
        user_object, flag = models.UserInfo.objects.get_or_create(phone=phone)
        # 4. 生成token
        token = str(uuid.uuid4())
        now = timezone.now()
        models.UserToken.objects.update_or_create(user=user_object, defaults={'token': token, 'created': now})
        cache.set(token, user_object, 60 * 60 * 24 * 7)


        return Response({"status": True, "data": {"token": token, 'phone': phone}})
class CredentialView(APIView):

    def get(self,request,*args,**kwargs):
        # -*- coding: utf-8 -*-

        # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
        #auth = oss2.Auth('yourAccessKeyId', 'yourAccessKeySecret')
        # 如果使用STS授权，则填写从STS服务获取的临时访问密钥（AccessKey ID和AccessKey Secret）以及安全令牌（SecurityToken）。
        auth = oss2.StsAuth(ALIBABA_OSS_ACCESS_KEY_ID, ALIBABA_OSS_ACCESS_KEY_SECRET, ALIBABA_SECURITYTOKEN)

        # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
        # 填写Bucket名称，例如examplebucket。
        bucket = oss2.Bucket(auth, ALIBABA_BUCKET_ENDPOINT, ALIBABA_OSS_BUCKET_NAME)
        # 填写Object完整路径，例如exampledir/exampleobject.txt。Object完整路径中不能包含Bucket名称。
        object_name = request.query_params.get('object_name')

        # 指定Header。
        headers = dict()
        # 指定Content-Type。
        # headers['Content-Type'] = 'text/txt'
        # 指定存储类型。
        # headers["x-oss-storage-class"] = "Standard"

        # 生成上传文件的签名URL，有效时间为60秒。
        # 生成签名URL时，OSS默认会对Object完整路径中的正斜线（/）进行转义，从而导致生成的签名URL无法直接使用。
        # 设置slash_safe为True，OSS不会对Object完整路径中的正斜线（/）进行转义，此时生成的签名URL可以直接使用。
        url = bucket.sign_url('PUT', object_name, 60, slash_safe=True, headers=headers)
        print('签名URL的地址为：', url)

        # 通过签名URL上传文件，以requests为例说明。
        # 填写本地文件路径，例如D:\\exampledir\\examplefile.txt。
        # requests.put(url, data=open('D:\\exampledir\\examplefile.txt', 'rb').read(), headers=headers)

        return Response(url)
class ImageCodeView(APIView):
    def get(self,request,*args,**kwargs):
        # 调用check_code函数生成验证码图片和验证码字符串
        image,code_string =check_code()
        print(code_string)
        # 写入到自己的session中
        request.session['image_code'] = code_string
        # 给session设置60s的过期时间
        request.session.set_expiry(6000)

        response = HttpResponse(content_type="image/jpeg")
        image.save(response, "JPEG")

        return response
class LogoutView(APIView):
    def post(self, request):
        # 清除用户的 token
        request.user.token.delete()

        # 清除用户的 session
        request.session.flush()

        # 返回响应
        return Response({"status": True, "message": "注销成功"})

























