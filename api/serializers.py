# -*- coding:utf-8 -*-
# @Author   ：kobe
# @time     ：2020/8/12 14:06
# @File     ：serializers.py
# @Software : PyCharm


from . import views
from rest_framework import serializers,exceptions
from rest_framework.serializers import ModelSerializer
from django.conf import settings
from .models import User,Books,Publish

# 序列化组件为每个model类通过一套序列化工具类
# 序列化组件的工作方式与django forms非常相似
class UserSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    sex = serializers.IntegerField()
    # 序列化提供给前台的字段个数由后台决定，可以少提供
    # 但是提供的数据库对应的字段，名字一定要与数据库字段相同
    # icon = serializers.ImageField()

    # 自定义序列化属性
    # 属性名随意，值由固定的命名规范方法提供
    # get_属性名(self, 参与序列化的model对象)
    # 返回值是自定义序列化属性的值
    gender = serializers.SerializerMethodField()
    def get_gender(self, obj):
        # print(obj, type(obj))
        # choice类型的解释型值 get_字段_display() 来访问
        return obj.get_sex_display()

    icon = serializers.SerializerMethodField()
    def get_icon(self, obj):
        return '{}{}{}'.format('http://127.0.0.1:8000', settings.MEDIA_URL, str(obj.icon))

class UserDelSerializers(serializers.Serializer):
    # 1)哪些字段必须反序列化
    # 2)字段都有哪些安全校验
    # 3)哪些字段需要额外提供校验
    # 4)哪些字段间存在联合校验
    # 注: 反序列化字段都是用来入库的，不会出现自定义方法属性，会出现可以设置校验规则的自定义属性(re_pwd)
    name = serializers.CharField(
        max_length=15,
        min_length=5,
        error_messages={
            "min_length": '最小长度不得低于5个字符'
        }
    )
    pwd = serializers.CharField()
    phone = serializers.CharField(required=False)
    sex = serializers.IntegerField(required=False)

    # 自定义有校验规则的反序列化字段
    re_pwd = serializers.CharField(required=True)

    # 总结
    # name,pwd,re_pwd为必填项字段
    # phone，sex为非必填项字段
    # 五个字段都必须提供完整的校验规则


    # 局部钩子 validate_要校验的字段名（self, 当前要校验字段的值）
    def validate_name(self, value):
        if 'j' in value.lower():
            raise exceptions.ValidationError("名字非法")
        return value

    def validate_sex(self, value):
        if not isinstance(value, int):
            raise exceptions.ValidationError("只能输入int类型")
        # if value != 1 :
        #     raise exceptions.ValidationError("只能输入男和女")
        return value
    # def validate_phone(self, value):
    #

    # 全局钩子 validate(self, 系统与局部钩子校验通过的所有数据)
    def validate(self, attrs):
        pwd = attrs.get('pwd')
        re_pwd = attrs.pop('re_pwd')
        if pwd != re_pwd:
            raise exceptions.ValidationError({"pwd&re_pwd": "两次密码输入不一致"})
        return attrs

    # 要完成新增，需要自己重写created方法
    def create(self, validated_data):
        # 尽量在所有校验规则完毕之后，数据可以直接入库
        return User.objects.create(**validated_data)

# 总结
# 1）设置必填与选填序列化字段，设置校验规则
# 2）为需要额外校验的字段提供局部钩子函数，如果该字段不入库，且不参与全局钩子校验，可以将值取出校验
# 3）为有联合关系的字段们提供全局钩子函数，如果某些字段不入库，可以将值取出校验
# 4）重写create方法，完成校验通过的数据入库工作，得到新增的对象

class PublishModelSerializers(ModelSerializer):

    class Meta:
        model = Publish
        fields = ('name', 'address')

class BookModelSerializers(ModelSerializer):

    publish = PublishModelSerializers()

    class Meta:
        # 序列化类关联的model类型
        model = Books
        fields = ('name', 'price', 'author_list', 'publish')
        # fields = '__all__'
        # exclude = ('id', 'is_deleted', 'create_time')

        depth = 1  # 自动连表深度

class BookModelDeserializers(ModelSerializer):

    class Meta:
        model = Books
        # 有默认值的字段不用
        fields = ('name', 'price', 'publish', 'authors')
        # extra_kwargs 用来完成反序列化字段的 系统校验规则
        extra_kwargs = {
            'name': {
                'required': True,
                'min_length': 1,
                'error_messages': {
                    'required': '必填项',
                    'min_length': '太短'
                }
            }
        }

    def validate_name(self, value):
        # 重复的书名判断
        # if Books.objects.filter(name=value):
        #     raise exceptions.ValidationError('书名已存在')
        # 书名不能包含g字符
        if 'g' in value.lower():
            raise exceptions.ValidationError('该书不能出版')
        return value

    def validate(self, attrs):
        publish = attrs.get("publish")
        name = attrs.get('name')
        if Books.objects.filter(name=name, publish=publish):
            raise exceptions.ValidationError('该书已存在')
        return attrs

