import oss2
import random
import uuid

from django.shortcuts import redirect
from rest_framework.reverse import reverse

from utils.auth import LoginAuth, IsVipUser
from utils.imagecode import check_code
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_redis import get_redis_connection
from django.http import HttpResponse, FileResponse, Http404
from MyServer import models
from utils.oss.aliYunOSS import get_download_video_url, get_upload_audio_url
from utils.sms.msg import send_message
from MyServer.serializer.account import MessageSerializer, LoginSerializer, RegisterSerializer

from ServerTest.settings import ALIBABA_OSS_ACCESS_KEY_ID, ALIBABA_OSS_ACCESS_KEY_SECRET, ALIBABA_BUCKET_ENDPOINT, \
    ALIBABA_SECURITYTOKEN, ALIBABA_OSS_BUCKET_NAME

from rest_framework.generics import ListAPIView, get_object_or_404
from UserSession.models import Speaker, VirtualPerson, BackGround, FrontGround
from UserSession.serializer.account import SpeakerSerializer, VirtualPersonSerializer, BackGroundSerializer, \
    FrontGroundSerializer, DisplayVideoSerializer, UploadVideoAudioSerializer, DownloadAudioSerializer


# Create your views here.
# TODO:感觉可以优化一下，把所有的get请求都放在一个类里面，然后根据参数来判断是哪个请求


class SpeakerListView(ListAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer


class VirtualPersonListView(ListAPIView):
    queryset = VirtualPerson.objects.all()
    serializer_class = VirtualPersonSerializer


class BackGroundListView(ListAPIView):
    queryset = BackGround.objects.all()
    serializer_class = BackGroundSerializer


class FrontGroundListView(ListAPIView):
    queryset = FrontGround.objects.all()
    serializer_class = FrontGroundSerializer


class ImageView(APIView):
    model_map = {
        'speaker': Speaker,
        'virtualperson': VirtualPerson,
        'background': BackGround,
        'foreground': FrontGround,
    }

    def get(self, request, model_name, file_id, format=None):
        model = self.model_map.get(model_name.lower())
        if model is None:
            raise Http404
        obj = get_object_or_404(model, image_id=file_id)
        return FileResponse(obj.image)


class DisplayVideoView(APIView):
    class VirtualPersonView(APIView):
        def post(self, request, format=None):
            serializer = DisplayVideoSerializer(data=request.data)
            if serializer.is_valid():
                virtual_person = get_object_or_404(VirtualPerson, id=serializer.validated_data['id'])
                return redirect(reverse('video-view', args=[virtual_person.video_id]))
            else:
                return Response(serializer.errors, status=400)


# TODO ：
class VideoView(APIView):
    pass


# #TODO ： 上传录音
# class TestUploadView(APIView):
#     def get(self, request, format=None):
#         # -*- coding: utf-8 -*-
#         import oss2
#
#         # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
#         auth = oss2.Auth('yourAccessKeyId', 'yourAccessKeySecret')
#         # 如果使用STS授权，则填写从STS服务获取的临时访问密钥（AccessKey ID和AccessKey Secret）以及安全令牌（SecurityToken）。
#         # auth = oss2.StsAuth('yourAccessKeyId', 'yourAccessKeySecret', 'yourToken')
#
#         # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
#         # 填写Bucket名称，例如examplebucket。
#         bucket = oss2.Bucket(auth, 'yourEndpoint', 'examplebucket')
#         # 填写Object完整路径，例如exampledir/exampleobject.txt。Object完整路径中不能包含Bucket名称。
#         object_name = 'exampledir/exampleobject.txt'
#
#         # 指定Header。
#         headers = dict()
#         # 填写Object的versionId。
#         headers["versionId"] = "CAEQARiBgID8rumR2hYiIGUyOTAyZGY2MzU5MjQ5ZjlhYzQzZjNlYTAyZDE3****"
#
#         # 生成上传文件的签名URL，有效时间为60秒。
#         # 生成签名URL时，OSS默认会对Object完整路径中的正斜线（/）进行转义，从而导致生成的签名URL无法直接使用。
#         # 设置slash_safe为True，OSS不会对Object完整路径中的正斜线（/）进行转义，此时生成的签名URL可以直接使用。
#         url = bucket.sign_url('PUT', object_name, 60, slash_safe=True, headers=headers)
#         print('签名URL的地址为：', url)
#         return Response('test')
class UploadVideoAudioView(APIView):
    authentication_classes = [LoginAuth]
    permission_classes = [IsAuthenticated, IsVipUser]

    def get(self, request):
        serializer = UploadVideoAudioSerializer(data=request.query_params)
        if serializer.is_valid():
            filename = request.user.phone + '/Audio/' + serializer.file_name
            url, headers = get_upload_audio_url(filename, serializer.file_type)
            return Response({'url': url, 'headers': headers})
        else:
            return Response(serializer.errors, status=400)


class DownloadAudioView(APIView):
    authentication_classes = [LoginAuth]
    permission_classes = [IsAuthenticated, IsVipUser]

    def get(self, request):
        serializer = DownloadAudioSerializer(data=request.query_params)
        if serializer.is_valid():
            user = models.UserInfo.objects.get(phone=request.user.phone)
            files = user.files.all()
            filename = request.user.phone + '/Audio/' + serializer.file_name
            if filename not in files.values_list('filename', flat=True):
                return Response({'error': '该文件不存在'}, status=404)
            url = get_download_video_url(filename)
            return Response({'url': url})
        else:
            return Response(serializer.errors, status=400)

