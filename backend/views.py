#coding=utf8
from __future__ import unicode_literals,print_function

from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/', {'username': request.user.username})
        else:
            return render(request, 'login.html', {'error': '账号或密码'})

@require_http_methods(['GET'])
def logout(request):
    auth.logout(request)
    return redirect('/user/login')

@require_http_methods(['POST'])
def register(request):
    return redirect('index.html', {'username': request.user.username})

@login_required
@require_http_methods(['GET'])
def index(request):
    return render(request, 'index.html', {'username': request.user.username})





