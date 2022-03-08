from django.db import models

# Create your models here.

from django.db import models
from my_admin.models import Book
from django.utils import timezone


# 创建商品种类
# class Category(models.Model):
#     db_table = 'shop_category'
#     kind = models.CharField(max_length=255)
#
# # 商品
# class Product(models.Model):
#     db_table = 'shop_product'
#
#     category = models.ForeignKey(Category, related_name="category_product", on_delete=models.CASCADE)  #
#     name = models.CharField(max_length=30)
#     price = models.FloatField()
#     author = models.CharField(max_length=100)
#     publisher = models.CharField(max_length=100)
#     abstract = models.TextField()
#     img_url = models.CharField(max_length=150)
#     pub_date = models.DateField()

#购物车
from my_book.models import UserInfo


class Cart(models.Model):
    db_table = 'shop_cart'
    # cid = models.AutoField(primary_key=True)          # id
    userinfo = models.ForeignKey(UserInfo,related_name='userinfo_cart',on_delete=models.CASCADE)  # 外键 用户
    product = models.ForeignKey(Book,related_name='book_cart',on_delete=models.CASCADE)     # 外键 商品
    pnum = models.IntegerField()                         # 数量
    sumprice = models.CharField(max_length=64)           # 总价格
    #时间
    time = models.DateField(auto_now_add=True) # 创造时间


class PayCart(models.Model):
    db_table = 'shoppaycart'
    # id = models.AutoField(primary_key=True)          # id
    cart = models.ForeignKey(Cart,related_name='carttopay',on_delete=models.CASCADE)  # 外键 用户


# order
class myorder(models.Model):
    # order_id = models.AutoField(primary_key=True)  # 订单id
    ordernum = models.CharField(max_length=32)  # 订单编号
    userinfo = models.ForeignKey(UserInfo, related_name='userinfo_order', on_delete=models.CASCADE)  # 外键
    product = models.ForeignKey(Book, related_name='book_order', on_delete=models.CASCADE)  # 外键 商品
    allprice = models.FloatField()  # 商品总价
    allpnum = models.IntegerField()  # 总数量
    paydate = models.DateTimeField  # 日期
    address = models.CharField(max_length=255)  # 收货地址