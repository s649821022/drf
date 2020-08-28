# -*- coding:utf-8 -*-
# @Author   ：kobe
# @time     ：2020/8/12 14:06
# @File     ：serializers.py
# @Software : PyCharm


from . import views
from rest_framework import serializers,exceptions
from rest_framework.serializers import ModelSerializer, ListSerializer
from django.conf import settings
from .models import User,Books,Publish


class BookListSerializer(ListSerializer):
    def update(self, instance, validated_data):
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance

class BookModelSerializers(ModelSerializer):
    class Meta:
        model = Books
        fields = ('publish', 'authors', 'name', 'price', 'img', 'author_list', 'publish_name')
        extra_kwargs = {
            'name': {
                'required': True,
                'min_length': 1,
                'error_messages': {
                    'required': '必填项',
                    'min_length': '太短'
                }
            },
            'publish': {
                'write_only': True
            },
            'authors': {
                'write_only': True
            },
            'author_list': {
                'read_only': True
            },
            'publish_name': {
                'read_only': True
            },
            'img': {
                'read_only': True
            }
        }

        list_serializer_class = BookListSerializer

    def validate_name(self, value):
        if 'g' in value.lower():
            raise exceptions.ValidationError('该书不能出版')
        return value

    def validate(self, attrs):
        publish = attrs.get("publish")
        name = attrs.get('name')
        if Books.objects.filter(name=name, publish=publish):
            raise exceptions.ValidationError('该书已存在')
        return attrs


