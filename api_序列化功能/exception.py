# -*- coding:utf-8 -*-
# @Author   ：kobe
# @time     ：2020/8/10 17:05
# @File     ：exception.py
# @Software : PyCharm


from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK

def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        # print("{} - {} - {}") % (context['view'], context['request'].method, exc)
        return Response({
            'detail': '服务器错误'
        }, status=HTTP_200_OK, headers={})
    return response



