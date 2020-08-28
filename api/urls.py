# -*- coding:utf-8 -*-
# @Author   ：kobe
# @time     ：2020/8/6 17:21
# @File     ：urls.py
# @Software : PyCharm


from django.urls import path
from django.conf.urls import url,re_path
from . import views
from rest_framework.routers import SimpleRouter
from django.conf.urls import include
app_name = 'api'

router = SimpleRouter()
router.register('v6/books', views.BookModelViewSet)


urlpatterns = [
    path('v1/books/', views.BookAPIView.as_view()),
    url(r'^v1/books/(?P<pk>.*)/$', views.BookAPIView.as_view()),

    path('v2/books/', views.BookGenericAPIView.as_view()),
    url(r'^v2/books/(?P<pk>.*)/$', views.BookGenericAPIView.as_view()),

    path('v3/books/', views.BookMixinGenericAPIView.as_view()),
    url(r'^v3/books/(?P<pk>.*)/$', views.BookMixinGenericAPIView.as_view()),

    path('v4/books/', views.BookListGenericAPIView.as_view()),
    url(r'^v4/books/(?P<pk>.*)/$', views.BookListGenericAPIView.as_view()),

    path('v5/books/', views.BookGenericViewSet.as_view({"get": "my_get_list"})),
    url(r'^v5/books/(?P<pk>.*)/$', views.BookGenericViewSet.as_view({"get": "my_get_obj"})),

    path('v6/books/', views.BookModelViewSet.as_view({"get": "my_get_list", "post": "create"})),
    url(r'^v6/books/(?P<pk>.*)/$', views.BookModelViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"})),

    # url(r'^', include(router.urls)),
]

# urlpatterns.extend(router.urls)