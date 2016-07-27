#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals,print_function

import moment

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from backend.models import *
from ._func import *

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
@transaction.atomic
def register(request):
    account = request.POST['account']
    username = request.POST['username']
    password = request.POST['password']
    number = request.POST['number']
    xclass = request.POST['xclass']

    # 简单的表单校验
    if not (account and username and password and number and xclass and image):
        return HttpResponse('确认填写的信息完整！', status=400)

    # 创建用户
    if account in User.objects.filter(username=account):
        return HttpResponse('用户存在', status=400)

    new_user = User()
    new_user.username = account
    new_user.set_password(password)
    new_user.is_active = True
    new_user.save()

    new_extuser = ExtUser(user=new_user, student_number=number, xclass=xclass, name=username)
    new_extuser.save()

    return redirect('/user/login')


@login_required
@require_http_methods(['GET'])
def index(request):
    account = request.user.username
    real_name = request.user.user_ext.name
    student_number = request.user.user_ext.student_number
    xclass = request.user.user_ext.xclass

    now_user_activities = request.user.user_ext.activities.order_by('-created_at')
    for ac in now_user_activities:
        ac.format_time = moment.date(ac.created_at).format("YYYY-MM-DD hh:mm:ss A")

    paginator = Paginator(now_user_activities, 5)
    page = request.GET.get('page', 1)

    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        activities = paginator.page(1)

    first = False
    try:
        previous_page = activities.previous_page_number()
    except EmptyPage:
        first = True
        previous_page = 1 

    last = False
    try:
        next_page = activities.next_page_number()
    except EmptyPage:
        last = True
        next_page = paginator.num_pages 

    return render(request, 'index.html', {
        'account': account, 'username': real_name,
        'xclass': xclass, 'number': student_number,
        'activities': activities.object_list, 'previous_page': previous_page,
        'next_page': next_page, 'first': first, 'last': last})


@login_required
@require_http_methods(['GET', 'POST']) 
@transaction.atomic
def profile(request):
    if request.method == 'GET':
        logined_user = request.user 
        return render(request, 'profile.html', {'user': logined_user})
    if request.method == 'POST':
        return redirect('/')

