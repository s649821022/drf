from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Book,User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import APISettings
from . import serializers

class BookView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:  # 群查
            book_obj_list = Book.objects.all()
            book_list = []
            for obj in book_obj_list:
                dic = {}
                dic['title'] = obj.title
                dic['price'] = obj.price
                book_list.append(dic)
            return JsonResponse({
                'status': 0,
                'msg': 'ok',
                'result': book_list
            }, json_dumps_params={'ensure_ascii': False})
        else:
            book_dic = Book.objects.filter(pk=pk).values('title', 'price').first()
            if book_dic:
                return JsonResponse({
                    'status': 0,
                    'msg': 'ok',
                    'result': book_dic
                }, json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({
                    'status': 1,
                    'msg': 'fail',
                }, json_dumps_params={'ensure_ascii': False})
        # return JsonResponse('get_ok', safe=False)
    def post(self, request, *args, **kwargs):
        print(request.POST.dict())
        try:
            book_obj = Book.objects.create(**request.POST.dict())
            # print(book_obj)
            if book_obj:
                return JsonResponse({
                    'status': 0,
                    'msg': 'ok',
                    'results': {'title': book_obj.title, 'price': book_obj.price}
                }, json_dumps_params={'ensure_ascii': False})
        except:
            return JsonResponse({
                'status': 1,
                'msg': '参数错误',
            }, json_dumps_params={'ensure_ascii': False})

        return JsonResponse({
            'status': 2,
            'msg': '新增失败',
        }, json_dumps_params={'ensure_ascii': False})

from rest_framework.parsers import JSONParser,MultiPartParser,FormParser
class Test(APIView):

    def get(self, request, *args, **kwargs):
        # url拼接参数
        print(request._request.GET)  # 二次封装方式
        print(request.GET)  # 兼容
        print(request.query_params)  # 拓展
        return Response('drf get ok')

    def post(self, request, *args, **kwargs):
        # print(request._request.POST)  # 二次封装方式
        # print(request.POST)  # 兼容
        print(request.data)  # 拓展、兼容性最强，三种数据方式都可以
        print(request.query_params)
        return Response('drf post ok')

from rest_framework.renderers import JSONRenderer
class Test2(APIView):

    # 局部配置
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    renderer_classes = [JSONRenderer]
    def get(self, request, *args, **kwargs):
        return Response('drf get ok')

    def post(self, request, *args, **kwargs):
        print(request.data)  # 拓展、兼容性最强，三种数据方式都可以
        print(request.query_params)
        return Response('drf post ok')

class UserView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                # 用户对象不能直接作为数据返回给前台
                user_obj = User.objects.get(pk=pk)
                # 序列化一下
                user_ser = serializers.UserSerializer(user_obj).data
                print(user_ser, type(user_ser))
                return Response({
                    'status': 0,
                    'msg': '成功',
                    'results': user_ser
                })
            except:
                return Response({
                    'status': 2,
                    'msg': '用户不存在'
                })
        else:
            # 用户对象列表(queryset)不能直接作为数据返回给前台
            user_obj_list = User.objects.all()
            user_ser = serializers.UserSerializer(user_obj_list, many=True).data
            return Response({
                'status': 0,
                'msg': 0,
                'results': user_ser
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        # 数据是否合法，（增加对象需要一个字典对象）
        if not isinstance(request_data, dict) or request_data == {}:
            return Response({
                'status': 1,
                'msg': '数据类型错误'
            })
        # 数据类型合法，但数据内容不一定合法，需要校验数据,校验（参与反序列化）的数据需要赋值给data
        book_ser = serializers.UserDelSerializers(data=request_data)
        # 序列化对象调用is_valid方法完成校验，校验失败的失败信息都会被存储在序列化对象.errors中
        if book_ser.is_valid():
            # 校验通过
            book_obj = book_ser.save()
            print('book_obj:', book_obj)
            return Response({
                'status': 0,
                'msg': 'ok',
                'results': serializers.UserSerializer(book_obj).data
                # 'results': ''
            })
        else:
            # 校验失败
            return Response({
                'status': 1,
                'msg': book_ser.errors
            })

# 总结
# 1)book_ser = serializers.UserDelSerializers(data=request_data)  # 数据必须赋值给data
# 2)book_ser.is_valid()  # 结果为 通过 | 不通过
# 3)不通过返回book_ser.errors给前台，通过book_ser.save() 得到新增的对象，再正常返回