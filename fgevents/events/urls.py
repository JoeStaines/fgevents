from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create/$', views.createevent, name="events-createevent"),
    url(r'^$', views.index, name="events-index"),
]