#TODO: 注册云，开通云短信。



from alibabacloud_tea_openapi import models as open_api_models

from alibabacloud_dysmsapi20170525 import models as dysmsapi_models



from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client

from Tea.exceptions import UnretryableException
from alibabacloud_tea_util import models as util_models


from ServerTest.settings import ALIBABA_SMS_CONFIG


def send_message(phone,random_code):

    try:
        # print(phone)
        # phone = "{}{}".format("+86", phone)
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=ALIBABA_SMS_CONFIG['access_key_id'],
            # 必填，您的 AccessKey Secret,
            access_key_secret=ALIBABA_SMS_CONFIG['access_key_secret']
        )
        client = Dysmsapi20170525Client(config)

        client.endpoint = f'dysmsapi.aliyuncs.com'
        send_sms_request = dysmsapi_models.SendSmsRequest(
            sign_name='阿里云短信测试',
            template_code='SMS_154950909',
            phone_numbers=phone,
            template_param='{{"code": "{}"}}'.format(random_code)
        )
        runtime = util_models.RuntimeOptions()
        send_resp = client.send_sms_with_options(send_sms_request, runtime)
        code = send_resp.body.code



        if code == "OK":
            return True


    except UnretryableException as error:

        # 如有需要，请打印 error

        print(error.inner_exception.code)
        print(error.inner_exception.message)