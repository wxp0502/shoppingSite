from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Commodity, MyCommodity


# Create your views here.

def index(request):
    return render(request, 'mall/index.html')


def homepage(request):
    goods = Commodity.objects.all()
    context = {'goods': goods}
    return render(request, 'mall/home.html', context)


@login_required()
def cart(request):
    """ 显示用户的购物车 """
    my_cart = MyCommodity.objects.filter(owner=request.user).order_by('date_added')
    context = {'my_cart': my_cart}
    return render(request, 'mall/cart.html', context)
