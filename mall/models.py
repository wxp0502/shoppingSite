from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Commodity(models.Model):
    # 商品图片；名称；描述；价格；销量；上市日期
    photo = models.ImageField(upload_to='mall/images')
    name = models.CharField(max_length=50)
    description = models.TextField(default='物美价廉')
    price = models.FloatField(default=9)
    sales = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MyCommodity(models.Model):
    # 购物车中商品的 数量；商品种类；拥有者；加入时间
    amount = models.PositiveIntegerField(default=1)
    goods = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.goods.name

    # 计算该商品的总价
    def total_cost(self):
        return self.amount * self.goods.price


class ReceivedCommodity(models.Model):
    # 购买日期；拥有者，名字，数量，价格，商品图片
    bought_date = models.DateTimeField(auto_now_add=True)
    # 每个用户有自己的订单查看
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # 注意：删除了 My Commodity 但是，收到的不会消失，所以不能用外键
    name = models.CharField(max_length=50)
    amount = models.PositiveIntegerField()
    price = models.FloatField()
    photo = models.ImageField(upload_to='mall/images')

    def __str__(self):
        return self.name

    # 计算总价
    def total_cost(self):
        return self.price * self.amount
