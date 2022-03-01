import base64
import os
import random
import time

from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponse, reverse
from . import models

# Create your views here.
def index(request):
    return render(request, 'badmin/admin_index.html')


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
        return HttpResponse('<script>alert("添加成功");location.href="' + url + '";</script>')
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

def admin_product_list(request):
    products = models.Book.objects.filter().all()
    paginator = Paginator(products, 2)
    page = request.GET.get('page_num')
    try:
        current_page = paginator.page(page)  # 指定 page 页面中的内容
    except PageNotAnInteger:  # 传入参数不为整数，显示第一页
        current_page = paginator.page(1)
    except EmptyPage:  # 参数为空，显示最后一页面
        current_page = paginator.page(paginator.num_pages)
    data = {
        'products': current_page,
        'page': current_page,
        'page_num': page,
        'paginator': paginator
    }
    return render(request, 'badmin/product_list.html',data)

# def admin_product_list(request):
#     data = models.Book.objects.all()
#     path = 'badmin/product_list.html'
#     return page(request, data, 2, path)
#
# def page(request,data,pagenum,path):
#     # 实例化分页类
#     paginator = Paginator(data,pagenum)
#     # 获取当前页码
#     page_num = int(request.GET.get('page_num',1))
#     print(page_num)
#     # 获取当前页码的数据
#     pagedata = paginator.page(page_num)
#     # 获取总页码数
#     pagecount = paginator.num_pages
#     # 获取页码范围,循环
#     pagerange = paginator.page_range
#     # 对页码进行判断,防止页码小于1或大于最大页码数
#     if page_num < 1:
#         page_num = 1
#     if page_num > pagecount:
#         page_num = pagecount
#     # 返回页码循环数,在模板里遍历
#     if page_num <= 5:
#         page_list = pagerange[:10]
#     elif page_num + 5 > pagecount:
#         page_list = pagerange[-10:]
#     else:
#         page_list = pagerange[page_num-5:page_num+4]
#     # 返回分页后的数据,分页范围循环,当前页码
#     return render(request,path,{'products': pagedata.object_list,'page':pagedata})

def prodelete(request):
    id = request.GET.get("p_id")
    obj = models.Book.objects.get(id=id)
    os.remove('.'+ obj.img_url)
    obj.delete()
    # return admin_product_list(request)
    url = reverse('product_list')
    return HttpResponse('<script>alert("删除成功");location.href="' + url + '";</script>')

def modproduct(request):
    id = request.GET.get('p_id')
    data = models.Book.objects.get(id = id)
    print(data.name)

    return render(request, 'badmin/modproduct.html', {'book': data})


def modproductdata(requset):
    data = requset.POST.dict()
    print(data)
    data.pop('csrfmiddlewaretoken')
    img = requset.FILES.get('img_url')
    if img:
        filename = save_img(requset)
        os.remove('.' + data['old_url'])
        data['img_url'] = filename
    else:
        data['img_url'] = data.old_url
    data.pop('old_url')
    print(data)
    obj = models.Book.objects.filter(id=data['id'])
    obj.update(**data)
    url = reverse('product_list')
    return HttpResponse('<script>alert("修改成功");location.href="' + url + '";</script>')













