# -*- coding:utf-8 -*-
# @Author   ：kobe
# @time     ：2020/8/24 17:26
# @File     ：response.py
# @Software : PyCharm


from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

class APIResponse(Response):

    def __init__(self, data_status=0, data_msg='ok', results=None, http_status=None, headers=None, exception=False, **kwargs):
        # data的初始状态
        data = {
            'statusCode': data_status,
            'message': data_msg
        }
        # data的响应数据体
        if results is not None:
            data['results'] = results
        # data的其他数据
        # if kwargs is not None:
        #     for k, v in kwargs.items():
        #         self[k] = v
        # data.update(kwargs)
        if kwargs is not None:
            for k, v in kwargs.items():
                setattr(kwargs, k, v)
        super().__init__(data=data, status=http_status, headers=headers, exception=exception)
