from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Commodity, MyCommodity


# Create your views here.

def index(request):
    return render(request, 'mall/index.html')


def homepage(request):

    if request.method == 'POST':
        print('---------------')
        gid = request.POST['gid']
        print(gid)
        mys = MyCommodity.objects.all()
        flag = 0
        for m in mys:
            # print(m.goods.id, end= '--')
            print(type(m.goods.id))
            print(m.goods.id == gid)
            print(type(gid))

            if m.goods.id == eval(gid):
                print('================')
                m.amount += 1
                m.save()
                flag += 1
        if flag == 0:
            new_my = MyCommodity(amount=1,
                                 goods=Commodity.objects.get(id=gid),
                                 owner=request.user)
            new_my.save()

    goods = Commodity.objects.all()
    context = {'goods': goods}
    return render(request, 'mall/home.html', context)


@login_required()
def cart(request):
    """ 显示用户的购物车 """
    my_cart = MyCommodity.objects.filter(owner=request.user).order_by('date_added')
    context = {'my_cart': my_cart}
    return render(request, 'mall/cart.html', context)
