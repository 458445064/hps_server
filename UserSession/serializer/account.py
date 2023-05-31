from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django_redis import get_redis_connection
from UserSession import models


# TODO: 感觉可以优化一下
class SpeakerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Speaker
        fields = ['id', 'name', 'gender', 'age', 'language', 'description', 'image_url']

    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)


class VirtualPersonSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.VirtualPerson
        fields = ['id', 'name', 'pose', 'image_url', 'video_url']

    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)

    def get_video_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.video.url)


class BackGroundSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.BackGround
        fields = ['id', 'name', 'image_url']

    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)


class FrontGroundSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.FrontGround
        fields = ['id', 'name', 'image_url']

    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)


class DisplayVideoSerializer(serializers.ModelSerializer):
    class VirtualPersonIdSerializer(serializers.Serializer):
        id = serializers.IntegerField()

        def validate_id(self, value):
            if not models.VirtualPerson.objects.filter(id=value).exists():
                raise serializers.ValidationError('该视频不存在')
            return value


class UploadVideoAudioSerializer(serializers.Serializer):
    file_type = serializers.FileField()
    file_name = serializers.FileField()

    def validate_file_type(self, value):
        # 如果file_type不是mp3或者wav格式的话，就报错
        if value not in ['mp3', 'wav']:
            raise ValidationError('文件格式不正确')
        return value


class DownloadAudioSerializer(serializers.Serializer):
    file_name = serializers.FileField()

    def validate_file_name(self, value):
        # 如果file_name为空的话，就报错
        if not value:
            raise ValidationError('文件名不能为空')
        return value
