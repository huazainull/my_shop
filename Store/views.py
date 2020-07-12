from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from Qshop.views import *
# Create your views here.
# def index(request):
#     return render(request,'store/index.html')
from Store.models import *


# def index(request):
#     cookie = request.COOKIES.get('username')
#     if cookie:
#         return render(request, 'store/base.html')
#     else:
#         return HttpResponseRedirect('/Store/login/')


# 商品首页
@Valid_Store #index=Valid_Store(index)
def index(request):
    numlist=[]
    type=Type.objects.filter(parert=0)
    for t in type:
        coms=t.commodity_set.all()
        numlist.append(len(coms))
    commoditys=Commodity.objects.all()

    return render(request,'store/index.html',locals())


def ajax(request):
    result={}
    names=[]
    nums=[]
    type=Type.objects.filter(parert=0)
    for t in type:
        names.append(t.name)
        coms=t.commodity_set.all()
        nums.append(len(coms))
    result["nmaes"]=names
    result["nums"]=nums
    return JsonResponse(result)



# 登录页面
def login(request):
    if request.method == 'POST' and request.POST:#判断是否post请求
        username=request.POST.get('username')
        password = request.POST.get('password')
        store=Store.objects.filter(login_name=username).first()#从数据库中查找用户名
        if store:
            from_password=setPassword(password)#对密码进行加密
            db_password=store.password
            if from_password==db_password:#加密后的密码与数据库比对
                response=HttpResponseRedirect('/Store/index')
                response.set_cookie('username',store.login_name)#设置cookie
                return response#返回首页

    return render(request,'store/login.html')

# 注册页面
def register(request):
    if request.method=='POST' and request.POST:
        data=request.POST
        img=request.FILES.get('logo')#图片获取注意用FILES

        store=Store()#实例化一个店铺对象
        store.store_name=data.get('store_name')
        store.login_name = data.get('login_name')
        store.password = setPassword(data.get('password'))
        store.email = data.get('email')
        store.phone = data.get('phone')
        store.address = data.get('address')
        store.logo = img
        store.save()#创建店铺后保存
        return HttpResponseRedirect('/Store/login/')#注册后返回到登录页面
    return render(request,'store/register.html')

# 注销
def logout(request):
    response=HttpResponseRedirect('/Store/login/')
    response.delete_cookie('username')#删除cookie
    return response


from django.core.paginator import Paginator


# def typelist(request):
#
#     typelists=Type.objects.all()
#
#     return render(request,'store/listtype.html',locals())


# 商品列表展示
@Valid_Store
def commodityList(request,type,page):#type上下架类型，page页码
    page_int=int(page)
    if type=='down':
        comlist = Commodity.objects.filter(delete_falg='true').order_by('-commodity_data')
    else:
        comlist = Commodity.objects.filter(delete_falg='false').order_by('-commodity_data')
    paginator=Paginator(comlist,10)#将商品分页展示，10个一页
    page_data=paginator.page(page_int)#获取page页的数据，传入到前端页面进行渲染
    if page_int<4:
        page_range=range(1,6)
    else:
        page_range=paginator.page_range[page_int-3:page_int+2]
    return render(request,'store/commodityList.html',{'page_data':page_data,'page_range':page_range,'type':type})

# 上下架功能
@Valid_Store
# def soldCommodity(request,type,id):
def soldCommodity(request,id):
    url=request.META.get('HTTP_REFERER')#获取请求之前的url
    com=Commodity.objects.get(id=int(id))
    # if type=='down':
    #     com.delete_falg='true'
    # else:
    #     com.delete_falg = 'false'
    # com.save()
    if com.delete_falg=='true':
        com.delete_falg='false'
    else:
        com.delete_falg='true'
    com.save()
    return HttpResponseRedirect(url)

# 添加商品类型
def addtype(request):
    types = Type.objects.all()
    if request.method=='POST':
        data=request.POST
        name=data.get('name')
        parent=data.get('types')
        picture=request.FILES.get('picture')

        t=Type()
        t.name=name
        t.parert=parent
        t.picture=picture
        t.save()
        # return HttpResponseRedirect('Store/comlist/up/1')


    return render(request,'store/addtype.html',locals())

# 添加商品
@Valid_Store
def addCommodity(request):
    type=Type.objects.all()#获取所有类型
    if request.method=='POST':
        data=request.POST
        name=data.get('name')
        price=data.get('price')
        number=data.get('number')
        picture=request.FILES.get('picture')
        datas=data.get('data')
        safe=data.get('safe')
        types=data.get('types')
        address=data.get('address')
        content=data.get('content')

        c=Commodity()
        c.commodity_name=name
        c.commodity_id='6666666'
        c.commodity_price = price
        c.commodity_number = number
        c.commodity_picture = picture
        c.commodity_data = datas
        c.commodity_safe_data = safe
        c.commodity_adress = address
        c.commodity_content = content
        c.delete_falg='false'
        c.type=Type.objects.get(id=int(types)) #添加外键
        # c.save()
        store_login_name=request.COOKIES.get('username')#通过cookie获取的店铺登录名称
        c.shop=Store.objects.get(login_name=store_login_name) #通过登录名称获取商店数据
        #多对多时候
        # store = Store.objects.get(login_name=store_login_name)  # 通过登录名称获取商店数据
        # c.shop.add(store)#添加数据到商品当中
        c.save()#再次保存

        return HttpResponseRedirect('/Store/comlist/up/1')

    return render(request,'store/addCommodity.html',locals())

# fr
    # type=['海产','肉类','粮油','蛋奶','水果','海外']
    # for i in type:om django.http import HttpResponse
# def addData(request):
    #     ty=Type()
    #     ty.name=i
    #     ty.parert=0
    #     ty.save()


    # import random
    # commodity=['牛肉','大虾','樱桃','鲜奶','大米','牛排']
    # country='蒙古、朝鲜、韩国、日本、菲律宾、越南、老挝、柬埔寨、缅甸、泰国、马来西亚、文莱、新加坡、印度尼西亚、东帝汶'.split('、')
    # for i in range(1000):
    #     com=Commodity()
    #     c=random.choice(country)
    #     com.commodity_name = c+random.choice(commodity)
    #     com.commodity_id =str(i).zfill(9)
    #     com.commodity_price =random.randint(100,1000)
    #     com.commodity_number =1000
    #     com.commodity_data = '%s-%s-%s'%(random.randint(2000,2019),random.randint(1,12),random.randint(1,28))
    #     com.commodity_safe_data = 120
    #     com.commodity_adress = c
    #     com.commodity_content = '嘎嘣脆'
    #
    #     com.delete_falg = 'false'
    #     com.type = Type.objects.get(id=random.randint(1,6))
    #     com.save()
    #     com.shop.add(Store.objects.get(login_name='wdl'))
    #     com.save()

    # return HttpResponse('保存成功')


# def order_list(request):
#     """
#     c查询所有商品
#
#     """
#     store=Store.objects.get(login_name=request.COOKIES.get("username"))
#     order_list=store.orderresource_set.all()
#     return render(request,'store/order_list.html',locals())