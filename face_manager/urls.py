from django.conf.urls import url
from django.contrib import admin
from backend import views as backend_views
from backend import apis

urlpatterns = [
    url(r'^$', backend_views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^user/login$', backend_views.login),
    url(r'^user/logout$', backend_views.logout),
    url(r'^user/register$', backend_views.register),
    url(r'^user/profile$', backend_views.profile),
    url(r'^api/activity$', apis.activity),
    url(r'^api/charts$', apis.charts),
]
