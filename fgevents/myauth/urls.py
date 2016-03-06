from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.log_in, name='myauth-login'),
    url(r'^logout/$', views.log_out, name='myauth-logout'),
    url(r'^register/$', views.register, name='myauth-register'),
]