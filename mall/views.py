from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Commodity, MyCommodity
import django.template.defaultfilters

# Create your views here.

def index(request):
    return render(request, 'mall/index.html')


def homepage(request):
    if request.method == 'POST':
        # print('---------------')
        gid = request.POST['gid']
        # print(gid)
        mys = MyCommodity.objects.filter(owner=request.user).order_by('date_added')
        flag = 0
        for m in mys:
            print(m.goods.id, end='--')
            print(type(m.goods.id))
            print(m.goods.id == gid)
            print(type(gid))

            if m.goods.id == eval(gid):
                print('================')
                m.amount += 1
                m.save()
                flag += 1
        if flag == 0:
            print('what ?')
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
    print('cart view yes')
    for m in my_cart:
        print(m.goods.name)
    return render(request, 'mall/cart.html', context)


@login_required()
def send_email(request):
    context = {}
    if request.method == 'POST':
        my_id = request.POST['my_id']
        goods = []
        # print('------------------------')
        for i in MyCommodity.objects.all():
            # print('22222')
            if i.id == eval(my_id):
                # print('3333333333')
                goods.append(i)
        context = {'goods': goods}
    return render(request, 'mall/send_email.html', context)


@login_required()
def purchased(request):
    if request.method == 'POST':
        email = request.POST['email']
        goods = request.POST['goods']
        send_mail(
            subject='感想购买WMall商品，祝您生活愉快！！！',
            message=r'shit you',
            from_email='2396469068@qq.com',
            recipient_list=[fr'{email}'],
            fail_silently=False
        )
    return render(request, 'mall/purchased.html')
