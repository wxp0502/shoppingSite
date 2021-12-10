from django.shortcuts import render

from .models import Commodity


# Create your views here.

def index(request):
    return render(request, 'mall/index.html')


def homepage(request):
    goods = Commodity.objects.all()
    context = {'goods': goods}
    return render(request, 'mall/home.html', context)
