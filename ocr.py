# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List
import json

from alibabacloud_ocr_api20210707.client import Client as ocr_api20210707Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_darabonba_stream.client import Client as StreamClient
from alibabacloud_ocr_api20210707 import models as ocr_api_20210707_models


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> ocr_api20210707Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'ocr-api.cn-hangzhou.aliyuncs.com'
        return ocr_api20210707Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = Sample.create_client('LTAI5tPjviEybwHkpi4PuSxY', 'hZtfKSMfU8vn9o4xJeEC3DdAJ7hEFp')
        body_syream = StreamClient.read_from_file_path(args)
        # body_syream = StreamClient.read_from_string(args)
        recognize_advanced_request = ocr_api_20210707_models.RecognizeAdvancedRequest(
            body=body_syream
        )
        # 复制代码运行请自行打印 API 的返回值
        content = client.recognize_advanced(recognize_advanced_request)
        data = content.body.data
        data_json = json.loads(data)
        return data_json['content']

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client('LTAI5tPjviEybwHkpi4PuSxY', 'hZtfKSMfU8vn9o4xJeEC3DdAJ7hEFp')
        body_syream = StreamClient.read_from_file_path('/home/mocuili/Downloads/dfe80a0a-14e4-4061-9f1e-8c53da3a00ac.jpg')
        recognize_advanced_request = ocr_api_20210707_models.RecognizeAdvancedRequest(
            body=body_syream
        )
        # 复制代码运行请自行打印 API 的返回值
        await client.recognize_advanced_async(recognize_advanced_request)


if __name__ == '__main__':
    Sample.main(sys.argv[1:])
