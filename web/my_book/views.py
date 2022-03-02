from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse

from . import models

# Create your views here.
def index(request):
    return render(request, 'bshop_user/login.html')

def register(request):
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


def login():
    return None


def logout():
    return None


def editaddress():
    return None


def getaddress():
    return None


def editpassword():
    return None


def personalinfo():
    return None