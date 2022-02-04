from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet, basename="addresses")

urlpatterns = [
    path('', views.index, name='index'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('updatecart/', views.updatecart, name='updatecart'),
    path('basket/', views.basket, name='basket'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('orders/', views.orders, name='orders'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('addcomment/', views.addcomment, name='addcomment'),
    path('delcomment/', views.delcomment, name='delcomment'),
    path('pagewitherror/', views.pagewitherror, name='pagewitherror'),
    path('product/<int:id>', views.product, name='product'),
    path('myaccount', views.myaccount, name='myaccount'),
    path('changeemail', views.changeemail, name='changeemail'),
    path('stocklevel/', views.stocklevel, name='stocklevel'),
    path('corstest', views.corstest, name='corstest'),
    path('getcsrftoken', views.getcsrftoken, name='getcsrftoken'),
    path('testcsrftoken', views.testcsrftoken, name='testcsrftoken'),
    path('gallery', views.gallery, name='gallery'),
    path('email_csp_report/', views.email_csp_report, name='email_csp_report'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
         namespace='rest_framework')),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('oauthapi/hello', views.OAuthResource.as_view()),
]
