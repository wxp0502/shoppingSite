from django.db import models


# Create your models here.

class Commodity(models.Model):
    photo = models.ImageField(upload_to='mall/images')
    name = models.CharField(max_length=50)
    price = models.FloatField()
    inventory = models.IntegerField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    pass