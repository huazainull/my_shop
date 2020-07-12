# Generated by Django 2.2.1 on 2019-05-22 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='BuyCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity_name', models.CharField(max_length=32)),
                ('commodity_id', models.IntegerField()),
                ('commodity_price', models.FloatField()),
                ('commodity_number', models.IntegerField()),
                ('commodity_picture', models.ImageField(upload_to='buyer/images')),
                ('buyuser_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_name', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('username', models.CharField(blank=True, max_length=32, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=32)),
                ('photo', models.ImageField(upload_to='buyer/images')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=32)),
                ('money', models.FloatField()),
                ('status', models.CharField(max_length=32)),
                ('date', models.DateTimeField(auto_now=True)),
                ('user_address', models.ForeignKey(on_delete=True, to='Buyer.Address')),
                ('user_id', models.ForeignKey(on_delete=True, to='Buyer.Buyer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity_name', models.CharField(max_length=32)),
                ('commodity_id', models.IntegerField()),
                ('commodity_price', models.FloatField()),
                ('commodity_number', models.IntegerField()),
                ('commodity_picture', models.ImageField(upload_to='buyer/images')),
                ('small_money', models.FloatField()),
                ('order_id', models.ForeignKey(on_delete=True, to='Buyer.Order')),
                ('store_id', models.ForeignKey(on_delete=True, to='Store.Store')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='buyer_id',
            field=models.ForeignKey(on_delete=True, to='Buyer.Buyer'),
        ),
    ]
