from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Book,User,Books,Publish,AuthorDetail,Author
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.settings import APISettings
from utils.response import APIResponse
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework.generics import ListCreateAPIView,UpdateAPIView
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from . import serializers


class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        book_query = Books.objects.filter(is_deleted=False).all()
        book_data = serializers.BookModelSerializers(book_query, many=True).data
        return APIResponse(results=book_data)

# GenericAPIView是继承APIView的，使用完全兼容APIView
# 重点：GenericAPIView在APIView的基础上完成了哪些事情
# 1)get_queryset(): 从类属性queryset中获得model的queryset数据
# 2)get_object(): 从类属性queryset中获得model的queryset数据，再通过有名分组pk确定唯一操作对象
# 3)get_serializer():从类属性serializer_class中获得serializer的序列化类
class BookGenericAPIView(GenericAPIView):

    queryset = Books.objects.filter(is_deleted=False)
    serializer_class = serializers.BookModelSerializers

    #自定义主键的有名分组名
    lookup_field = 'pk'

    # 单取
    def get(self, request, *args, **kwargs):
        book_query = self.get_object()
        book_data = self.get_serializer(book_query).data
        return APIResponse(results=book_data)

    # 群查
    # def get(self, request, *args, **kwargs):
    #     book_query = self.get_queryset()
    #     book_data = self.get_serializer(book_query, many=True).data
    #     return APIResponse(results=book_data)

# 1)mixins有五个工具类文件，一共提供了五个工具类，六个工具方法：单查、群查、单增、单删、单整体改、单局部改
# 2）继承工具类可以简化请求函数的实现体，但是必须继承GenericAPIView，需要GenericAPIView类提供的几个类属性和方法
# 3）工具类的工具方法返回值都是Response类型对象，如果要格式化数据格式再返回给前台，可以通过response.data 难道工具方法返回的Response
class BookMixinGenericAPIView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericAPIView):

    queryset = Books.objects.filter(is_deleted=False)
    serializer_class = serializers.BookModelSerializers

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            response = self.retrieve(request, *args, **kwargs)  # 单查
        else:
            response = self.list(request, *args, **kwargs)  # 群查
        return APIResponse(results=response.data)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)  # 单增
        return APIResponse(results=response.data)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)  # 群改
        return APIResponse(results=response.data)

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)  # 单改
        return APIResponse(results=response.data)



class BookListGenericAPIView(ListCreateAPIView, UpdateAPIView):
    queryset = Books.objects.filter(is_deleted=False)
    serializer_class = serializers.BookModelSerializers


# 1)视图集都是优先继承ViewSetMixin类，再继承一个视图类（GenericAPIView或APIView）
# 2)ViewSetMixin提供了重写的as_view()方法，继承视图集的视图类，配置路由时调用as_view()必须传入 请求-函数名 映射关系字典
#   eg: url(r'^v5/books/(?P<pk>.*)/$', views.BookGenericViewSet.as_view({"get": "my_get_obj"})),
#   表示get请求会交给my_get_obj视图函数处理

class BookGenericViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Books.objects.filter(is_deleted=False)
    serializer_class = serializers.BookModelSerializers

    def my_get_obj(self, request, *args, **kwargs):
        response = self.retrieve(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def my_get_list(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return APIResponse(results=response.data)

"""
GenericAPIView与APIView 作为两大继承视图的区别
1)GenericViewSet和ViewSet都继承了ViewSetMixin，as_view都可以配置 请求-函数 映射
2)GenericViewSet继承的是GenericAPIView视图类，用来完成标准的model类操作接口
3)ViewSet继承的是APIView视图类，用来完成不需要model类参与，或是非标准的model类操作接口
    post请求在标准的model类操作下就是新增接口，登陆的post不满足
    post请求验证码接口，不需要model类的参与
    案例：登陆的post请求，并不是完成数据的新增，只是用post提交数据，得到的结果也不是登陆的用户信息，而是登陆的认证信息
"""

class BookModelViewSet(ModelViewSet):
    queryset = Books.objects.filter(is_deleted=False)
    serializer_class = serializers.BookModelSerializers

    def my_get_list(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return APIResponse(1, "删除失败")
        instance.is_deleted = True
        instance.save()
        return APIResponse(0, '删除成功')

