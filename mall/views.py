from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Commodity, MyCommodity, ReceivedCommodity


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
            # print(m.goods.id, end='--')
            # print(type(m.goods.id))
            # print(m.goods.id == gid)
            # print(type(gid))

            if m.goods.id == eval(gid):
                # print('================')
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
    if request.method == 'POST':
        print('remove ')
        remove = request.POST['remove']
        my_id = request.POST['my_id']
        print(type(remove))
        if eval(remove) == 1:
            print('111111111111111')
            temp = MyCommodity.objects.get(id=my_id)
            if temp.amount == 1:
                temp.delete()
            else:
                temp.amount -= 1
                temp.save()
    print('=========')
    my_cart = MyCommodity.objects.filter(owner=request.user).order_by('date_added')
    context = {'my_cart': my_cart}
    print('cart view yes')
    for m in my_cart:
        print(m.goods.name)
    return render(request, 'mall/cart.html', context)


@login_required()
def send_email(request):
    context = {}
    total_cost = 0
    if request.method == 'POST':
        buy_all = request.POST.get('buy_all')
        if buy_all and buy_all == 'yes':
            all_my = MyCommodity.objects.all()
            for a in all_my:
                total_cost += a.total_cost()
            context = {'all_my': all_my, 'total_cost': total_cost}

        else:
            my_id = request.POST['my_id']
            wanted = MyCommodity.objects.get(id=my_id)
            total_cost = wanted.total_cost()
            context = {'wanted': wanted, 'total_cost': total_cost}

    return render(request, 'mall/send_email.html', context)


@login_required()
def purchased(request):
    if request.method == 'POST':
        text = '您所购买的宝贝清单：\n'
        email = request.POST['email']
        wanted_id = request.POST.get('wanted_id')
        if wanted_id:
            wanted = MyCommodity.objects.get(id=wanted_id)
            text += f'{wanted.goods.name}   '
            text += f'数量:  {wanted.amount}    '
            text += f'总价:  ￥{wanted.total_cost()} \n'
            # 加入已购买的宝贝
            new_received = ReceivedCommodity(name=wanted.goods.name, amount=wanted.amount, price=wanted.goods.price)
            new_received.save()
            # 从购物车移出此商品
            wanted.delete()

        else:
            all_buy = MyCommodity.objects.all()
            for a in all_buy:
                text += f'{a.goods.name}   '
                text += f'数量:  {a.amount}    '
                text += f'总价:  ￥{a.total_cost()} \n'
                # 加入已购买的宝贝
                new_received = ReceivedCommodity(name=a.goods.name, amount=a.amount, price=a.goods.price)
                new_received.save()

            # 清除购物车
            MyCommodity.objects.all().delete()
        text += '欢迎下次使用，祝您生活愉快！！！' + '\n🎈🎈🎈✨✨✨'
        send_mail(
            subject='感谢使用WMall，您所购买的商品已送至门口，请及时取件',
            message=text,
            from_email='2396469068@qq.com',
            recipient_list=[fr'{email}'],
            fail_silently=False
        )
    return render(request, 'mall/purchased.html')


@login_required()
def received(request):
    all_received = ReceivedCommodity.objects.all()
    context = {'all_received': all_received}
    return render(request, 'mall/received.html', context)
