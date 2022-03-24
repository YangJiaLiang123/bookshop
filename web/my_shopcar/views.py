import datetime
import time
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from . import models
from my_admin.models import Book
from my_book.models import Address
# Create your views here.
from utils.alipay import AliPay


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


def cash_payment(request):
    cartlist = request.POST.get("cartlist")  # 支付的购物车id
    cartlist = cartlist.split('#')
    username = request.session.get('username')
    userinfo = models.UserInfo.objects.filter(username=username)[0]
    address = Address.objects.filter(userinfo=userinfo)[0]
    allcartpay = models.PayCart.objects.filter().all()
    if allcartpay != '':
        models.PayCart.objects.filter().all().delete()
    for i in cartlist:
        if i != '':
            obj = models.Cart.objects.filter(id=i).first()
            cartpay = models.PayCart(cart_id=obj.id)
            cartpay.save()
    allcart = models.Cart.objects.filter(userinfo=userinfo).all()
    print(allcart)
    Clist = models.PayCart.objects.filter().all()
    context = {
        'username': username,
        'curaddress': address.getFullAddress(),
        'allcart': allcart,
        'Clists': Clist
    }
    return render(request, 'bshop/pay.html', context)

alipay = AliPay(appid='2021000119639263', app_notify_url='http://127.0.0.1:8000/shop/checkPay/', app_private_key_path='my_shopcar/pay/keys/app_private_key.pem',
                 alipay_public_key_path='my_shopcar/pay/keys/alipay_public_key.pem', return_url='http://127.0.0.1:8000/shop/checkPay/', debug=True)

def pay_view(request):
    import uuid
    m = request.POST.get('m', 0)
    params = alipay.direct_pay(subject="购物商城", out_trade_no=str(uuid.uuid4().int)[:16], total_amount=str(m))
    print(params.split('&'))
    url = alipay.gateway + '?' + params
    return HttpResponseRedirect(url)


def checkPay(request):
    params = request.GET.dict()
    sign = params.pop('sign')
    if alipay.verify(params, sign):
        ordernum = params.get('out_trade_no')
        orderobj = models.myorder.objects.get(ordernum=ordernum)
        orderobj.static = '支付完成待发货'
        orderobj.save()
        carts = request.session.get('carts')
        for i in carts:
            cart = models.Cart.objects.get(id=i)
            cart.delete()
        del request.session['carts']
        return HttpResponse("success")
    del request.session['carts']
    return HttpResponse("fail")


def pay(request):
    import uuid
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    address = data.pop('address')
    allprice = 0
    allnum = 0
    carts = list(data.values())
    for i in data.values():
        allprice += float(models.Cart.objects.get(id=i).sumprice)
        allnum += models.Cart.objects.get(id=i).pnum
    data = {
        'ordernum': str(uuid.uuid4().int)[:16],
        'userinfo' : models.UserInfo.objects.get(username=request.session.get("username")),
        'allprice': allprice,
        'allpnum' : allnum,
        'paydate' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'address' : address,
    }
    orderobj = models.myorder(**data)
    orderobj.save()
    request.session['carts'] = carts
    params = alipay.direct_pay(subject="购物商城", out_trade_no=data.get('ordernum'), total_amount=str(allprice))
    url = alipay.gateway + '?' + params
    return HttpResponseRedirect(url)