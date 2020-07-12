from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
# Create your views here.
from Store.models import *
from Qshop.views import *


# 购物车
@Valid_Buyer
def carts(request):
    zongjia=0
    user_id=int(request.COOKIES.get('user_id'))
    shop_list=BuyCar.objects.filter(user_id=user_id)
    shops=[]
    for shop in shop_list:
        shops.append(
            {
            'id':shop.id,
            "commodity_name":shop.commodity_name,
            "commodity_id":shop.commodity_id,
            "commodity_price": shop.commodity_price,
            "commodity_number": shop.commodity_number,
            "commodity_picture": shop.commodity_picture,
            "total": shop.commodity_price*shop.commodity_number,
            }
        )
    jianshu=len(shops)
    for i in shops:
        zongjia=zongjia+i["total"]
    return render(request,'buyer/carts.html',locals())

# 注册
def register(request):
    if request.method=='POST':
        data=request.POST
        username=data.get('user_name')
        password = data.get('pwd')

        user=Buyer()
        user.login_name=username
        user.password=setPassword(password)
        user.save()
        return HttpResponseRedirect('/Buyer/login')
    return render(request,'buyer/register.html')

# 登录
def login(request):
    if request.method=='POST':
        data=request.POST
        username=data.get('username')
        password = data.get('pwd')

        user=Buyer.objects.filter(login_name=username).first()
        if user:
            db_password=user.password
            form_password=setPassword(password)
            if db_password==form_password:
                response=HttpResponseRedirect('/')
                response.set_cookie('username',user.login_name)
                response.set_cookie('user_id', user.id)
                return response

    return render(request,'buyer/login.html')

# 商品首页
@Valid_Buyer
def index(request):
    buycar=BuyCar.objects.all().filter(user_id=request.COOKIES.get("user_id"))
    num=len(buycar)
    types=Type.objects.filter(parert=0)
    result=[

    ]
    for t in types:#遍历每种类型，并且获取对应商品信息
        d={}
        d['type']=t
        d['data']=t.commodity_set.filter(delete_falg='false').order_by('-commodity_data')[:4]
        d['data1'] = t.commodity_set.filter(delete_falg='false').order_by('commodity_data')[:3]
        result.append(d)
    return render(request,'buyer/index.html',locals())

from django.core.paginator import Paginator

# 商品分页显示
@Valid_Buyer
def shop_list(request,type_id,page):
    buycar=BuyCar.objects.all().filter(user_id=request.COOKIES.get("user_id"))
    num=len(buycar)
    t_id=type_id
    page_int=int(page)
    coms=Type.objects.get(id=int(type_id)).commodity_set.filter(delete_falg='false')
    paginator = Paginator(coms, 10)
    page_data = paginator.page(page_int)

    if page_int < 4:
        page_range = range(1, 6)
    else:
        page_range = paginator.page_range[page_int - 3:page_int + 2]
    if page_int == 1:
        shangyiye=0
    else:
        shangyiye=page_int-1
    next_page=page_int+1
    return render(request,'buyer/list.html',locals())


from Buyer.models import *

# def search(request):
#     buycar=BuyCar.objects.all().filter(user_id=request.COOKIES.get("user_id"))
#     num=len(buycar)
#     com=Commodity.objects.all()
#     if request.method=='GET':
#         name=request.GET.get('shopname')
#         for c in com:
#             if c.commodity_name==name:
#                 id=c.id
#                 url="/Buyer/detail/"+str(id)
#                 return HttpResponseRedirect(url)
#
#     # return render(request,"buyer/search_shop.html",locals())

# 商品详情页
@Valid_Buyer
def detail(request,com_id):
    buycar=BuyCar.objects.all().filter(user_id=request.COOKIES.get("user_id"))
    num=len(buycar)
    com=Commodity.objects.get(id=int(com_id))
    if request.method=='POST':
        number=request.POST.get('number')
        car=BuyCar()
        car.commodity_name=com.commodity_name
        car.commodity_id=com.id
        car.commodity_price=com.commodity_price
        car.commodity_number=number
        car.commodity_picture=com.commodity_picture

        car.shop_id=com.shop.id#商品和店铺为多对一关系，直接商品.商铺.id获得店铺id
        # user=Buyer.objects.get(login_name=request.COOKIES.get('username'))
        # car.buyuser_id=user.id

        car.user_id= request.COOKIES.get('user_id')#通过COOKIES获得对应用户id
        car.save()
        return HttpResponseRedirect('/Buyer/carts')
    print(request.META.get("HTTP_REFERER"))
    return render(request,'buyer/detail.html',locals())

# 用户中心
def usercenter(request):
    buycar=BuyCar.objects.all().filter(user_id=request.COOKIES.get("user_id"))
    num=len(buycar)
    add_list=Address.objects.all()
    if request.method=='POST':
        data=request.POST
        recver=data.get('recver')
        address = data.get('address')
        phone = data.get('phone')

        addr=Address()
        addr.address=address
        addr.recver=recver
        addr.phone=phone
        addr.buyer_id=Buyer.objects.get(id=int(request.COOKIES.get('user_id')))
        addr.save()

    return render(request,'buyer/usercenter.html',locals())

# 添加订单地址
@Valid_Buyer
def place_order(request):
    buycar=BuyCar.objects.all().filter(user_id=request.COOKIES.get("user_id"))
    num=len(buycar)
    if request.method=='POST':
        address=Address.objects.all()
        car_shop_list=[]
        xiaoji=[]

        heji = 0
        for k,v in request.POST.items():
            if v == 'on':
                car_data=BuyCar.objects.get(id=int(k))
                x=car_data.commodity_price*car_data.commodity_number
                xiaoji.append(x)
                heji=heji+car_data.commodity_price*car_data.commodity_number
                car_shop_list.append(car_data)
        zongshu=len(car_shop_list)
        car_shop_list=enumerate(car_shop_list,1)
        car_shop_lists={
            "car_shop_list":car_shop_list,
            "xiaoji":xiaoji
        }
        return render(request,'buyer/place_order.html',locals())
    else:
        return HttpResponse('bad request method')


from django.http import JsonResponse
from Qshop.views import sendMessage,validCode

# 发送验证码
def sendCode(request):
    result = {"status": "error", "data": ""}
    if request.method == 'GET':
        recver=request.GET.get('recver')
        res=sendMessage(recver)
        if res=='ok':
            result['status']='success'
            result['data']='验证码发送成功'
        else:
            result['data']='发送失败'
    return JsonResponse(result)

# 验证验证码
def codeValid(request):
    result={}
    if request.method=='POST':
        email=request.POST.get('email')
        code=request.POST.get('code')
        result=validCode(email,code)
        if result['data']=='验证成功':
            return HttpResponseRedirect('/')
    return render(request,'buyer/validCode.html',locals())

import  datetime
from   Qshop.views import Pay

# 支付功能
def pay(request):
    if request.method=='GET' and request.GET:
        data=request.GET
        data_item=data.items()
        order=Order()
        order.user_address=Address.objects.get(id=1)
        order.status=0
        order.date=datetime.datetime.now()
        order.user_id=Buyer.objects.get(id=request.COOKIES.get('user_id'))
        order.save()
        order.order_number='sp'+str(order.id).zfill(10)
        order.save()
        money=0
        for k,v in data_item:
            if k.startswith('shop_'):
                car_id=int(v)
                data=BuyCar.objects.get(id=car_id)
                order_reource=OrderResource()
                order_reource.commodity_name=data.commodity_name
                order_reource.commodity_id = data.commodity_id
                order_reource.commodity_price = data.commodity_price
                order_reource.commodity_number = data.commodity_number
                order_reource.commodity_picture = data.commodity_picture
                order_reource.small_money = data.commodity_price*data.commodity_number
                order_reource.order_id = order
                order_reource.store_id = Store.objects.get(id=data.shop_id)
                order_reource.save()
                money+=order_reource.small_money
        order.money=money
        url=Pay(order.order_number,order.money)
        return HttpResponseRedirect(url)
        # return render_to_response(request,url)

# 购物车删除商品
def delete(request,id):
    url=request.META.get('HTTP_REFERER')
    buycar_com=BuyCar.objects.get(id=int(id))
    buycar_com.delete()
    return HttpResponseRedirect(url)