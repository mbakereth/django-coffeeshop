from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('youhavewon/', views.youhavewon, name='youhavewon'),
    path('youhavewonssl/', views.youhavewonssl, name='youhavewonssl'),
    path('iframe/', views.iframe, name='iframe'),
    path('cookies/<str:cookie>', views.cookies, name='cookies'),
    path('gettest/', views.gettest, name='gettest'),
    path('posttest/', views.posttest, name='posttest'),
    path('credtest/', views.credtest, name='credtest'),
    path('oauthcallback/', views.oauthcallback, name='oauthcallback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
