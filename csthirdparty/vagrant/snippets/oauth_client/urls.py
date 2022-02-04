from django.urls import path, include, re_path
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('youhavewon/', views.youhavewon, name='youhavewon'),
    path('cookies/<str:cookie>', views.cookies, name='cookies'),
    path('gettest/', views.gettest, name='gettest'),
    path('posttest/', views.posttest, name='posttest'),
    path('credtest/', views.credtest, name='credtest'),
    path('oauthcallback/', views.oauthcallback, name='oauthcallback'),
    path('oidc/', include('oidc_rp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
