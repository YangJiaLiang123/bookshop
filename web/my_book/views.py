from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse

from . import models

# Create your views here.
def index(request):
    return render(request, 'bshop/index.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'bshop_user/register.html')
    else:
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        data.pop('chb_agreement')
        data.pop('check_password')
        password = make_password(data.get('password'), None, 'pbkdf2_sha256')
        data['password'] = password
        obj = models.UserInfo(**data)
        obj.save()
        return render(request, 'bshop_user/login.html')

def register_tel(request):
    tel = request.GET.get('tel')
    count = models.UserInfo.objects.filter(telephone=tel).count()
    return JsonResponse({'count': count})

def register_exist(request):
    uname = request.GET.get('uname')
    count = models.UserInfo.objects.filter(username=uname).count()
    return JsonResponse({'count': count})


def login(request):
    if request.method == 'GET':
        return render(request, 'bshop_user/login.html')
    else:
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        data.pop('autologin')
        obj = models.UserInfo.objects.filter(username = data['username'])
        if obj.count() == 0:
            context = {'error_name': 1, 'error_pwd': 0, 'username': data['username'], 'password': data['password']}
            return render(request, 'bshop_user/login.html', context)
        else:
            if check_password(data.get('password'), obj[0].password):
                request.session['username'] = obj[0].username
                return render(request,'bshop/index.html',{'data': data})
            else:
                context = {'error_name': 0, 'error_pwd': 1, 'username': data['username'], 'password': data['password']}
                return render(request, 'bshop_user/login.html', context)


def logout(request):
    request.session.flush()
    url = reverse('bUser :login')
    return HttpResponse(f'<script>location.href="{url}";</script>')


def editaddress():
    return None


def getaddress(request):
    usename = request.session.get('username')
    
    return None


def editpassword(request):
    if request.method == 'GET':
        return render(request, 'bshop_user/editpwd.html')
    else:
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        obj = models.UserInfo.objects.filter(username=request.session.get('username'))
        print('121111', obj[0].username, obj[0].password)
        if check_password(data.get('oldpassword'), obj[0].password):
            password = make_password(data.get('newpassword'), None, 'pbkdf2_sha256')
            print(password)
            # obj[0].password = password
            # print(obj[0].password)
            # obj[0].save()
            obj.update(password=password)
            print(obj[0].password)
            request.session.flush()
            url = reverse('bUser :login')
            return HttpResponse('<script>alert("密码修改成功，请重新登录");location.href="'+url+'";</script>')
            # return render(request, 'bshop_user/editpwd.html')
        else:
            context = {'error_pwd': 1, 'oldpassword': '', 'newpassword': '', 'username': request.session.get('username')}
            return render(request, 'bshop_user/editpwd.html', context)


def personalinfo(request):
    username = request.session.get('username')
    print(username)
    obj = models.UserInfo.objects.filter(username = username)
    context = {
        'username': username,
        'telephone': obj[0].telephone,
        'email': obj[0].email
    }
    return render(request, 'bshop_user/personalinfo.html', context)







