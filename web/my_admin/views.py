import base64
import random
import time

from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, HttpResponse, reverse
from . import models

# Create your views here.
def index(request):
    return render(request, 'badmin/addproduct.html')


def adminlogin(request):
    if request.method == 'GET':
        return render(request, 'badmin/login.html')
    else:
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        print(data)
        obj = models.Users.objects.get(id=1)
        print(obj.username)
        if obj.username != data.get('username'):
            error = '用户名不存在'
            return render(request, 'badmin/login.html', {'tip': error})
        else:
            # password = make_password(data.get('password'), None, 'pbkdf2_sha256')
            # print(password)
            password = check_password(data.get('password'), obj.password)
            if password:
                return render(request, 'badmin/admin_index.html', {'userinfo': data})
            else:
                error = '密码输入错误'
                return render(request, 'badmin/login.html', {'tip': error})


def logout():
    return None


def imagemanage():
    return None


def imageupload():
    return None


def categorym():
    return None


def newfcategory():
    return None


def categorydelete():
    return None


def addproduct(request):
    if request.method == 'GET':
        return render(request, 'badmin/addproduct.html')
    else:
        data =request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        print(data)
        filename = save_img(request)
        data['img_url'] = filename
        print(data)
        obj = models.Book(**data)
        obj.save()
        url = reverse('product_list')
        return HttpResponse('<script>alert("成功");location.href="' + url + '";</script>')
        # return render(request, 'badmin/product_list.html')
        # return HttpResponse('ok')

def save_img(request):
    img = request.FILES.get('img_url')
    if img:
        a = str(img).split('.').pop()
        print(a)
        imgname = str(random.random() + time.time()) + '.' + a
        print(imgname)
        try:
            with open(f'./static/image/{imgname}','wb+') as f:
                for i in img.chunks():
                    f.write(i)
            filename = f'/static/image/{imgname}'
            return filename
        except:
            return False
    else:
        return ''

def newproduct():
    return None


def admin_product_list():
    return None


def prodelete():
    return None


def modproduct():
    return None


def modproductdata():
    return None