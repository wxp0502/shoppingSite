from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def register(request):
    # 如果不是 POST 请求，生成内置表单 UserCreationForm
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        # 使用内置表单 UserCreationForm 得到注册信息
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            # 保存新用户信息，并授权登录
            new_user = form.save()
            authenticate_user = authenticate(username=new_user.username,
                                             password=request.POST['password1'])
            login(request, authenticate_user)
            # 登录后重定向至商品主页
            return HttpResponseRedirect(reverse('mall:home'))
    context = {'form': form}
    return render(request, 'users/register.html', context)
