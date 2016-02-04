#coding=utf8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ExtUser(models.Model):
    user = models.OneToOneField(User, related_name='user_ext')
    student_number = models.CharField('学号', max_length=10, null=False, blank=False, primary_key=True)
    xclass = models.CharField('班级', max_length=100, default='')