import datetime

from django.http import HttpResponse
from django.shortcuts import render
from . import models


# Create your views here.
def index(request):

    data = models.Book.objects.all()[0:4]
    print(data)
    return render(request, 'bshop/index.html', {'data': data})


def prodetail(request):
    id = request.GET.get('pid')
    obj = models.Book.objects.get(id=id)
    username = request.session.get('username')

    return render(request, 'bshop/detail1.html', {'product': obj, 'username': username, 'discount': 8.8})


def addtocart(request):
    if request.method == 'POST':
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        username = request.session.get('username')
        userinfo = models.UserInfo.objects.get(username=username)
        product = models.Book.objects.get(id=data['id'])
        print(userinfo, product)
        sumprice = int(data['num']) * product.price
        creatTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        thiscart = models.Cart.objects.filter(product=product, userinfo=userinfo).count()
        print(thiscart)
        if thiscart == 0:
            cart = models.Cart(userinfo=userinfo, product=product, pnum=data['num'], sumprice=sumprice, time=creatTime)
            cart.save()
        carts = models.Cart.objects.filter(userinfo=userinfo).all()
        print(carts)
        return render(request, 'bshop/ShowCart.html', {'allcart': carts, 'allcartnum': carts.count()})


def getcartnum(request):
    return HttpResponse('ok')


def showCart(request):
    return render(request, 'bshop/ShowCart.html')


def add_goods():
    return None


def sub_goods():
    return None


def delCart():
    return None


def cash_payment():
    return None