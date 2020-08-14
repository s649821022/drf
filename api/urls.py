# -*- coding:utf-8 -*-
# @Author   ：kobe
# @time     ：2020/8/6 17:21
# @File     ：urls.py
# @Software : PyCharm


from django.urls import path
from django.conf.urls import url,re_path
from . import views

app_name = 'api'

urlpatterns = [
    path('books/', views.BookView.as_view()),
    url(r'^books/(?P<pk>.*)/$', views.BookView.as_view()),
    path('users/', views.UserView.as_view()),
    url(r'^users/(?P<pk>.*)/$', views.UserView.as_view()),
    path('test/', views.Test.as_view()),
    path('test2/', views.Test2.as_view()),


]
