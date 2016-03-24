from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<event_id>[0-9]+)/$', views.detail, name="events-detail"),
    url(r'^create/$', views.createevent, name="events-createevent"),
    url(r'^$', views.index, name="events-index"),
]