import oss2

from ServerTest.settings import ALIBABA_OSS_ACCESS_KEY_ID, ALIBABA_OSS_ACCESS_KEY_SECRET, ALIBABA_BUCKET_ENDPOINT, \
    ALIBABA_OSS_BUCKET_NAME


def get_upload_audio_url(file_name, file_type):
    # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
    auth = oss2.Auth(ALIBABA_OSS_ACCESS_KEY_ID, ALIBABA_OSS_ACCESS_KEY_SECRET)
    # 如果使用STS授权，则填写从STS服务获取的临时访问密钥（AccessKey ID和AccessKey Secret）以及安全令牌（SecurityToken）。
    # auth = oss2.StsAuth('yourAccessKeyId', 'yourAccessKeySecret', 'yourToken')

    # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    # 填写Bucket名称，例如examplebucket。
    bucket = oss2.Bucket(auth, ALIBABA_BUCKET_ENDPOINT, ALIBABA_OSS_BUCKET_NAME)
    # 填写Object完整路径，例如exampledir/exampleobject.txt。Object完整路径中不能包含Bucket名称。
    object_name = file_name

    # 指定Header。
    headers = dict()
    # 指定Content-Type。
    if file_type == 'wav':
        # 指定Content-Type。
        headers['Content-Type'] = "audio/wav"
    elif file_type == 'mp3':
        headers['Content-Type'] = "audio/mp3"

    # 指定存储类型。
    headers["x-oss-storage-class"] = "Standard"

    # 生成上传文件的签名URL，有效时间为60秒。
    # 生成签名URL时，OSS默认会对Object完整路径中的正斜线（/）进行转义，从而导致生成的签名URL无法直接使用。
    # 设置slash_safe为True，OSS不会对Object完整路径中的正斜线（/）进行转义，此时生成的签名URL可以直接使用。
    url = bucket.sign_url('PUT', object_name, 60, slash_safe=True, headers=headers)
    print('签名URL的地址为：', url)

    # 通过签名URL上传文件，以requests为例说明。
    # 填写本地文件路径，例如D:\\exampledir\\examplefile.txt。
    # requests.put(url, audioFile, headers=headers)

    return url, headers
def get_download_video_url(file_name):

        # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
        auth = oss2.Auth(ALIBABA_OSS_ACCESS_KEY_ID, ALIBABA_OSS_ACCESS_KEY_SECRET)
        # 如果使用STS授权，则填写从STS服务获取的临时访问密钥（AccessKey ID和AccessKey Secret）以及安全令牌（SecurityToken）。
        # auth = oss2.StsAuth('yourAccessKeyId', 'yourAccessKeySecret', 'yourToken')

        # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
        # 填写Bucket名称，例如examplebucket。
        bucket = oss2.Bucket(auth, ALIBABA_BUCKET_ENDPOINT, ALIBABA_OSS_BUCKET_NAME)
        # 填写Object完整路径，例如exampledir/exampleobject.txt。Object完整路径中不能包含Bucket名称。

        # 指定Header。
        headers = dict()
        # 指定Accept-Encoding。

        # 指定HTTP查询参数。
        params = dict()
        # 设置单链接限速，单位为bit，例如限速100 KB/s。
        # params['x-oss-traffic-limit'] = str(100 * 1024 * 8)
        # 指定IP地址或者IP地址段。
        # params['x-oss-ac-source-ip'] = "127.0.0.1"
        # 指定子网掩码中1的个数。
        # params['x-oss-ac-subnet-mask'] = "32"
        # 指定VPC ID。
        # params['x-oss-ac-vpc-id'] = "vpc-t4nlw426y44rd3iq4****"
        # 指定是否允许转发请求。
        # params['x-oss-ac-forward-allow'] = "true"

        # 生成下载文件的签名URL，有效时间为60秒。
        # 生成签名URL时，OSS默认会对Object完整路径中的正斜线（/）进行转义，从而导致生成的签名URL无法直接使用。
        # 设置slash_safe为True，OSS不会对Object完整路径中的正斜线（/）进行转义，此时生成的签名URL可以直接使用。
        url = bucket.sign_url('GET', file_name, 60, slash_safe=True, headers=headers, params=params)
        print('签名URL的地址为：', url)

        return url
