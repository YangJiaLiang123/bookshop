import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import models
from my_admin.models import Book

# Create your views here.
def index(request):
    datas = Book.objects.all()[0:4]
    username = request.session.get('username')
    data = {'username': username}
    return render(request, 'bshop/index.html', {'datas': datas, 'data': data})


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

        return render(request, 'bshop/ShowCart.html', {'allcart': carts, 'allcartnum': carts.count(), 'username': username})


def getcartnum(request):
    return HttpResponse('ok')


def showCart(request):
    username = request.session.get('username')
    userinfo = models.UserInfo.objects.get(username=username)
    carts = models.Cart.objects.filter(userinfo=userinfo).all()
    return render(request, 'bshop/ShowCart.html', {'allcart': carts, 'allcartnum': carts.count(), 'username': username})


def add_goods(request):
    product_id = request.POST.get('product_pid')
    username = request.session.get('username')
    userinfo = models.UserInfo.objects.get(username=username)
    product = models.Book.objects.get(id=product_id)
    cart = models.Cart.objects.filter(userinfo=userinfo, product=product).first()
    data = {}
    if cart:
        cart.sumprice = round(float(cart.sumprice) / cart.pnum * (cart.pnum + 1), 2)
        cart.pnum += 1
        cart.save()
        data['msg'] = '请求成功'
        return JsonResponse(data)

def sub_goods(request):
    product_id = request.POST.get('product_pid')
    username = request.session.get('username')
    userinfo = models.UserInfo.objects.get(username=username)
    product = models.Book.objects.get(id=product_id)
    cart = models.Cart.objects.filter(userinfo=userinfo, product=product).first()
    data = {}
    if cart:
        if cart.pnum==1:
            data['msg'] = '亲! 至少买一个吧'
        else:
            cart.sumprice = round (float(cart.sumprice) / cart.pnum * (cart.pnum - 1),2)
            cart.pnum -= 1
            cart.save()
            data['msg'] = '请求成功'
            return JsonResponse(data)
    else:
        data['msg'] = '请添加商品'
        return JsonResponse(data)

def delCart(request):
    id = request.GET.get('pid')
    username = request.session.get('username')
    userinfo = models.UserInfo.objects.get(username=username)
    product = models.Book.objects.get(id=id)
    obj = models.Cart.objects.get(userinfo=userinfo, product=product)
    obj.delete()
    return showCart(request)

def cash_payment():
    return None