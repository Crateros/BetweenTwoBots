from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^startbot$', views.startbot, name="startbot"),
  url(r'^stopbot$', views.stopbot, name="stopbot"),
  # url(r'^submit', views.submit)
]
