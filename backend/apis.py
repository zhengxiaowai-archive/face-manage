#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals,print_function

import json
import moment

from backend.models import Activity, ExtUser
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

@csrf_exempt
@require_http_methods(['POST', 'GET'])
@transaction.atomic
def activity(request):
    if request.method == 'POST':
        recogniton_activity = json.loads(request.body)
        student_id = recogniton_activity.get('student_id', None)
        is_ok = recogniton_activity.get('is_ok', None) 

        if (student_id == None or is_ok == None):
            return HttpResponse('paras error', status=400)

        try:
            current_user = ExtUser.objects.get(student_number=student_id) 
        except ObjectDoesNotExist:
            current_user = None

        if not current_user:
            return HttpResponse("not user", status=400)

        new_activity = Activity()
        new_activity.ext_user = current_user
        new_activity.is_ok = is_ok
        new_activity.save()

        return HttpResponse('OK')

@csrf_exempt
@require_http_methods(['GET'])
@transaction.atomic
def charts(request):
    user_activities = ExtUser.objects.get(user=request.user).activities.all()
    created_at_list = ExtUser.objects.get(
        user=request.user).activities.values('created_at')

    results = []
    for created_at in created_at_list:
        charts_item = {}
        fail = 0
        success = 0
        activity_time = created_at['created_at']
        one_day_activities = user_activities.filter(created_at=activity_time)
        fail = one_day_activities.filter(is_ok=False).count()
        success = one_day_activities.filter(is_ok=True).count()

        charts_item['time'] = moment.date(activity_time).format("MM-DD")
        charts_item['success'] = success
        charts_item['fail'] = fail
        results.append(charts_item)

    return JsonResponse({'faceRecognitionCounts': results}, status=200)
