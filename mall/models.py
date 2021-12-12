from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Commodity(models.Model):
    photo = models.ImageField(upload_to='mall/images')
    name = models.CharField(max_length=50)
    description = models.TextField(default='物美价廉')
    price = models.FloatField(default=9)
    sales = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MyCommodity(models.Model):
    amount = models.PositiveIntegerField(default=1)
    goods = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.goods.name

    def total_cost(self):
        return self.amount * self.goods.price


class ReceivedCommodity(models.Model):
    # 购买日期
    bought_date = models.DateTimeField(auto_now_add=True)
    # 每个用户有自己的订单查看
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # 注意：删除了 My Commodity 但是，收到的不会消失，所有不能用外键
    name = models.CharField(max_length=50)
    amount = models.PositiveIntegerField()
    price = models.FloatField()
    photo = models.ImageField(upload_to='mall/images')

    def __str__(self):
        return self.name

    def total_cost(self):
        return self.price * self.amount
