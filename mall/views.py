from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse

from .models import Commodity, MyCommodity, ReceivedCommodity

from .forms import CommodityForm


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
            # print('what ?')
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
        # print('remove ')
        remove = request.POST['remove']
        my_id = request.POST['my_id']
        # print(type(remove))
        if eval(remove) == 1:
            # print('111111111111111')
            temp = MyCommodity.objects.get(id=my_id)
            if temp.amount == 1:
                temp.delete()
            else:
                temp.amount -= 1
                temp.save()
    # print('=========')
    my_cart = MyCommodity.objects.filter(owner=request.user).order_by('date_added')
    context = {'my_cart': my_cart}
    # print('cart view yes')
    # for m in my_cart:
    #     print(m.goods.name)
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
            new_received = ReceivedCommodity(name=wanted.goods.name, amount=wanted.amount, price=wanted.goods.price,
                                             photo=wanted.goods.photo)
            new_received.owner = request.user
            new_received.save()
            # 给此商品 加 销量
            com = Commodity.objects.get(id=wanted.goods.id)
            com.sales += wanted.amount
            com.save()
            # 从购物车移出此商品
            wanted.delete()

        else:
            all_buy = MyCommodity.objects.all()
            for a in all_buy:
                text += f'{a.goods.name}   '
                text += f'数量:  {a.amount}    '
                text += f'总价:  ￥{a.total_cost()} \n'

                # 给此商品 加 销量
                com = Commodity.objects.get(id=a.goods.id)
                com.sales += a.amount
                com.save()
                # 加入已购买的宝贝
                new_received = ReceivedCommodity(name=a.goods.name, amount=a.amount, price=a.goods.price,
                                                 photo=a.goods.photo)
                new_received.owner = request.user
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
    # 记得加上用户独立的功能。。
    # 已经加上
    all_received = ReceivedCommodity.objects.filter(owner=request.user).order_by('bought_date')
    context = {'all_received': all_received}
    return render(request, 'mall/received.html', context)


@login_required()
def management(request):
    # print('---------')
    if request.method == 'POST':
        modify = request.POST.get('modify')
        if modify:
            pass
        else:  # 删除商品
            cd_id = request.POST.get('cd_id')
            if cd_id:
                temp = Commodity.objects.get(id=cd_id)
                temp.delete()
    commodities = Commodity.objects.all()
    # for c in commodities:
    #     print(c.name)
    context = {'commodities': commodities}
    return render(request, 'mall/management.html', context)


@login_required()
def add_commodity(request):
    if request.method == 'POST':
        form = CommodityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('mall:management'))
    else:
        form = CommodityForm()
    context = {'form': form}
    return render(request, 'mall/add_commodity.html', context)


@login_required()
def modify_commodity(request, cd_id):
    commodity = Commodity.objects.get(id=cd_id)

    if request.method == 'POST':
        form = CommodityForm(instance=commodity, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('mall:management'))
    else:
        form = CommodityForm(instance=commodity)
    context = {'form': form, 'commodity': commodity}
    return render(request, 'mall/modify_commodity.html', context)


@login_required()
def sales_statistics(request):
    all_received = ReceivedCommodity.objects.all()
    # 不同用户买的商品应该归类到一起
    all_sale = {}
    # 单价 ； 销量 ； 总价
    for a in all_received:
        if a.name in all_sale:
            all_sale[f'{a.name}'][0] = a.price  # 单价
            all_sale[f'{a.name}'][1] += a.amount  # 销量
            all_sale[f'{a.name}'][2] += a.price * a.amount  # 总价
        else:
            temp = {f'{a.name}': [a.price, a.amount, a.price * a.amount]}
            all_sale.update(temp)
    # for key in all_sale:
    #     print('-----------')
    #     print(key)
    #     print(all_sale[key][0])
    context = {'all_sale': all_sale}
    return render(request, 'mall/sales_statistics.html', context)


@login_required()
def user_statistics(request):
    # users = User.objects.all()    似乎没有什么必要
    # 订单记录
    received_c = ReceivedCommodity.objects.all().order_by('bought_date')
    indent = {}
    for r in received_c:
        if r.owner.email:
            continue  # 忽略管理员用户
        elif r.owner in indent:
            # 已经有此用户，加一列购买记录
            indent[r.owner].append([r.owner.username, r.name, r.price, r.amount, r.total_cost(), r.bought_date])
        else:
            temp = {r.owner: [[r.owner.username, r.name, r.price, r.amount, r.total_cost(), r.bought_date]]}
            indent.update(temp)
    # 购物车记录
    my_c = MyCommodity.objects.all().order_by('date_added')
    cart_record = {}
    for m in my_c:
        if m.owner.email:
            continue
        elif m.owner in cart_record:
            cart_record[m.owner].append([m.owner.username, m.goods.name, m.goods.price, m.amount, m.total_cost(), m.date_added])
        else:
            temp = {m.owner: [[m.owner.username, m.goods.name, m.goods.price, m.amount, m.total_cost(), m.date_added]]}
            cart_record.update(temp)

    context = {'indent': indent, 'cart_record': cart_record}
    return render(request, 'mall/user_statistics.html', context)
