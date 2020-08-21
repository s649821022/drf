from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Book,User,Books,Publish,AuthorDetail,Author
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import APISettings
from . import serializers

# class BookView(View):
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         if not pk:  # 群查
#             book_obj_list = Book.objects.all()
#             book_list = []
#             for obj in book_obj_list:
#                 dic = {}
#                 dic['title'] = obj.title
#                 dic['price'] = obj.price
#                 book_list.append(dic)
#             return JsonResponse({
#                 'status': 0,
#                 'msg': 'ok',
#                 'result': book_list
#             }, json_dumps_params={'ensure_ascii': False})
#         else:
#             book_dic = Book.objects.filter(pk=pk).values('title', 'price').first()
#             if book_dic:
#                 return JsonResponse({
#                     'status': 0,
#                     'msg': 'ok',
#                     'result': book_dic
#                 }, json_dumps_params={'ensure_ascii': False})
#             else:
#                 return JsonResponse({
#                     'status': 1,
#                     'msg': 'fail',
#                 }, json_dumps_params={'ensure_ascii': False})
#         # return JsonResponse('get_ok', safe=False)
#     def post(self, request, *args, **kwargs):
#         print(request.POST.dict())
#         try:
#             book_obj = Book.objects.create(**request.POST.dict())
#             # print(book_obj)
#             if book_obj:
#                 return JsonResponse({
#                     'status': 0,
#                     'msg': 'ok',
#                     'results': {'title': book_obj.title, 'price': book_obj.price}
#                 }, json_dumps_params={'ensure_ascii': False})
#         except:
#             return JsonResponse({
#                 'status': 1,
#                 'msg': '参数错误',
#             }, json_dumps_params={'ensure_ascii': False})
#
#         return JsonResponse({
#             'status': 2,
#             'msg': '新增失败',
#         }, json_dumps_params={'ensure_ascii': False})
class BookView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                book_obj = Books.objects.get(pk=pk, is_deleted=False)  # 查出来的对象
                book_data = serializers.BookModelSerializers(book_obj).data  #
            except:
                return Response({
                    'status': 1,
                    'msg': '书籍不存在'
                })
        else:
            book_query = Books.objects.filter(is_deleted=False).all()
            book_data = serializers.BookModelSerializers(book_query, many=True).data
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': book_data
        })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        book_ser = serializers.BookModelSerializers(data=request_data)
        # 当校验失败，马上终止当前视图方法，抛异常返回给前台
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.BookModelSerializers(book_obj).data
        })

class V2BookView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                book_obj = Books.objects.get(pk=pk, is_deleted=False)  # 查出来的对象
                book_data = serializers.V2BookModelSerializers(book_obj).data  #
            except:
                return Response({
                    'status': 1,
                    'msg': '书籍不存在'
                })
        else:
            book_query = Books.objects.filter(is_deleted=False).all()
            book_data = serializers.V2BookModelSerializers(book_query, many=True).data
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': book_data
        })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, dict):
            many = False
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                'status': 1,
                'msg': '数据有误',
            })
        book_ser = serializers.V2BookModelSerializers(data=request_data, many=many)
        # 当校验失败，马上终止当前视图方法，抛异常返回给前台
        book_ser.is_valid(raise_exception=True)
        book_result = book_ser.save()
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.V2BookModelSerializers(book_result, many=many).data
        })

    # 单删
    # 群删
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            pks = [pk]
        else:
            pks = request.data.get('pks')
        if Books.objects.filter(pk__in=pks, is_deleted=False).update(is_deleted=True):
            return Response({
                'status': 0,
                'msg': '删除成功'
            })
        return Response({
            'status': 1,
            'msg': '删除失败'
        })

    # 单整体该，对v2/books/(pk)传的数据是与model对应的字典name|price|publish|authors
    def put(self, request, *args, **kwargs):
        # 单群改
        request_data = request.data
        pk = kwargs.get('pk')
        old_book_obj = Books.objects.filter(pk=pk).first()
        # 目的：将众多数据的校验交给序列化类来处理 - 让序列化类扮演反序列化角色，校验成功后，序列化类来帮你入库
        book_ser = serializers.V2BookModelSerializers(instance=old_book_obj, data=request_data)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.V2BookModelSerializers(book_obj).data
        })
    #
    # def patch(self, request, *args, **kwargs):
    #     # 单局部改
    #     request_data = request.data
    #     pk = kwargs.get('pk')
    #     old_book_obj = Books.objects.filter(pk=pk).first()
    #     book_ser = serializers.V2BookModelSerializers(instance=old_book_obj, data=request_data, partial=True)
    #     book_ser.is_valid(raise_exception=True)
    #     book_obj = book_ser.save()
    #     return Response({
    #         'status': 0,
    #         'msg': 'ok',
    #         'results': serializers.V2BookModelSerializers(book_obj).data
    #     })

    """
    1)单体整体修改
    V2BookModelSerializers(
    instance=要被更新的对象，
    data=要更新的数据，
    partial=默认False，必须的字段全部参与校验
    )
    2)单体局部修改
    V2BookModelSerializers(
    instance=要被更新的对象，
    data=要更新的数据，
    partial=True，必须的字段都变为选填字段
    )
    注: partial设置True的本质就是使字段  required=True  校验规则失效
    """

    # 群体整改和群体局部改, 群改的数据格式化成pks=[要需要的对象主键标识] | request_Data=[每个要修改对象对应的修改数据]
    def patch(self, request, *args, **kwargs):
        request_data = request.data
        pk = kwargs.get('pk')
        if pk and isinstance(request_data, dict):  # 单改
            pks = [pk]
            request_data = [request_data]
        elif not pk and isinstance(request_data, list):  # 群改
            pks = []
            for dic in request_data:
                pk = dic.pop("pk", None)
                if pk:
                    pks.append(pk)
                else:
                    return Response({
                        'status': 1,
                        'msg': '数据有误'
                    })
        else:
            return Response({
                'status': 1,
                'msg': '数据有误'
            })

        # pks与request_data数据筛选
        # 1）将pks中的没有对应数据的pk与数据已删除的pk删除，request_data对应索引位上的数据也删除
        # 2）将合理的pks转换为objs

        objs = []
        new_request_data = []
        for index, pk in enumerate(pks):
            try:
                # pk对应的数据合理，将合理的对象存储
                obj = Books.objects.get(pk=pk, is_deleted=False)
                objs.append(obj)
                # 对应的索引数据就保存下来
                new_request_data.append(request_data[index])
            except:
                # pk对应的数据有误，将对应索引的data中的request_data删除
                continue


        book_ser = serializers.V2BookModelSerializers(instance=objs, data=new_request_data, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_objs = book_ser.save()

        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.V2BookModelSerializers(book_objs, many=True).data
        })

class PublishView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                publish_obj = Publish.objects.get(pk=pk, is_deleted=False)
                publish_data = serializers.PublishModelSerializers(publish_obj).data
                return Response({
                    'status': 0,
                    'msg': 'ok',
                    'results': publish_data
                })
            except:
                return Response({
                    'status': 1,
                    'msg': '出版社不存在'
                })
        else:
            publish_query = Publish.objects.filter(is_deleted=False).all()
            publish_data = serializers.PublishModelSerializers(publish_query, many=True).data
        return Response({
            'status': 1,
            'msg': '出版社不存在',
            'results': publish_data
        })



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

#