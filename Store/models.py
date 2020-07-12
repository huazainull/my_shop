from django.db import models

# Create your models here.
#店铺
class Store(models.Model):
    store_name=models.CharField(max_length=132)
    login_name = models.CharField(max_length=132)
    password = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=132)
    address = models.TextField()
    logo = models.ImageField(upload_to='store/images')

    def __str__(self):
        return self.store_name

#商品类型
class Type(models.Model):
    name=models.CharField(max_length=32)
    parert=models.IntegerField()
    picture=models.ImageField(upload_to='store/images',default='store/images/jpm.jpg')

    def __str__(self):
        return self.name

#商品
class Commodity(models.Model):
    commodity_name=models.CharField(max_length=32)
    commodity_id = models.CharField(max_length=32)
    commodity_price = models.FloatField()
    commodity_number = models.IntegerField()
    commodity_picture = models.ImageField(upload_to='store/images')
    commodity_data = models.DateField()
    commodity_safe_data = models.IntegerField()
    commodity_adress = models.TextField()
    commodity_content = models.TextField()

    delete_falg=models.CharField(max_length=32,default='false')
    type=models.ForeignKey(to=Type,on_delete=models.CASCADE)
    shop=models.ForeignKey(to=Store,on_delete=models.CASCADE)
    # shop=models.ManyToManyField(to=Store)

#商品图片类
class Picture(models.Model):
    image=models.ImageField(upload_to='store/images')
    commodity=models.ForeignKey(to=Commodity,on_delete=models.CASCADE)#一对一









