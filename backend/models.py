#coding=utf8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class ExtUser(models.Model):
    user = models.OneToOneField(User, related_name='user_ext')
    student_number = models.CharField('学号', max_length=10, null=False, blank=False, primary_key=True)
    xclass = models.CharField('班级', max_length=100, default='')
    name = models.CharField('姓名', max_length=100, default='')

    def __unicode__(self):
        return self.name

class Activity(models.Model):
    ext_user = models.ForeignKey(ExtUser, related_name='activities')
    created_at = models.DateTimeField(u'创建时间', default=timezone.now)
    is_ok = models.BooleanField(u'是否成功', default=False)

    def __unicode__(self):
        return "{name} | {created_at}".format(
            name=self.ext_user.name, created_at=self.created_at)