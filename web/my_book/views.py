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


def getaddress():
    return None


def editpassword():
    return None


def personalinfo():
    return None