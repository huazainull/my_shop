from django.db import models
from Store.models import *
# Create your models here.

# 用户 名字  手机 登录名 图片
# 购物车
# 订单
# 订单详情
# 地址

# 用户
class Buyer(models.Model):
    login_name=models.CharField(max_length=32)
    password=models.CharField(max_length=32)

    username=models.CharField(max_length=32,blank=True,null=True)
    #blank=True django默认值为空，可以在数据库不填数据
    #null=True django默认字段为空，在数据中写入null

    email=models.EmailField(blank=True,null=True)
    phone=models.CharField(max_length=32)

    photo=models.ImageField(upload_to='buyer/images')

# 购物车
class BuyCar(models.Model):
    commodity_name=models.CharField(max_length=32)
    commodity_id = models.IntegerField()
    commodity_price = models.FloatField()
    commodity_number = models.IntegerField()#购买商品数量
    commodity_picture = models.ImageField(upload_to='buyer/images')#商品图片
    shop_id = models.IntegerField(default=1)  # 店铺id
    user_id=models.IntegerField()#用户Id

# 地址
class Address(models.Model):
    address=models.TextField()
    phone=models.CharField(max_length=32)
    recver=models.CharField(max_length=32)
    buyer_id=models.ForeignKey(to=Buyer,on_delete=models.CASCADE)


# 订单
class Order(models.Model):
    # 状态：待支付（0），待确认（1），支付（2），确认收货（3）

    order_number=models.CharField(max_length=32,blank=True,null=True)#订单编号
    user_address=models.ForeignKey(to=Address,on_delete=models.CASCADE)
    money=models.FloatField(blank=True,null=True)
    status=models.IntegerField()
    date=models.DateTimeField(auto_now=True)
    user_id=models.ForeignKey(to=Buyer,on_delete=models.CASCADE)

# 订单详情
class OrderResource(models.Model):
    commodity_name = models.CharField(max_length=32)
    commodity_id = models.IntegerField()
    commodity_price = models.FloatField()
    commodity_number = models.IntegerField()  # 购买商品数量
    commodity_picture = models.ImageField(upload_to='buyer/images')  # 商品图片
    small_money=models.FloatField()
    order_id = models.ForeignKey(to=Order,on_delete=models.CASCADE)
    store_id=models.ForeignKey(to=Store,on_delete=models.CASCADE)

#验证码
class ValidCode(models.Model):
    code=models.CharField(max_length=32)
    loginName=models.CharField(max_length=32)
    time=models.FloatField()
    flag=models.CharField(max_length=4)

