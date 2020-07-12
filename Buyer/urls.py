from django.urls import path,re_path
from Buyer.views import *
urlpatterns=[
    path('index/',index),
    path('register/',register),
    path('login/', login),
    path('carts/', carts),
    path('place_order/', place_order),
    path('usercenter/', usercenter),
    path('sendCode/', sendCode),
    path('pay/', pay),
    path('search/', search),
    path('codeValid/', codeValid),
    re_path('delete/(\d+)', delete),
    re_path('detail/(\d+)', detail),
    re_path('list/(\d+)/(\d+)', shop_list),
]