from django.urls import path,re_path
from Store.views import *

urlpatterns=[
    path('typelist/',typelist),
    path('index/',index),
    path('login/',login),
    path('ajax/', ajax),
    path('register/',register),
    path('logout/',logout),
    path('order_list/', order_list),
    path('addCom/', addCommodity),
    path('addtype/', addtype),
    re_path('comlist/(\w+)/(\d+)', commodityList),
    # re_path('soldCom/(\w+)/(\d+)/', soldCommodity),
    re_path('soldCom/(\d+)/', soldCommodity),

]
urlpatterns+=[
    path('addData/', addData),
]