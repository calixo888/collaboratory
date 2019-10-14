from django.conf.urls import url
from django.urls import path
from . import views

app_name = "collaborator_app"

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^login/", views.user_login, name="login"),
    url("^logout/", views.user_logout, name="logout"),
    url("^register/", views.register, name="register"),
    url('^project/(?P<project_id>.+?)/$', views.project, name='project'),
    url('^create-project/$', views.create_project, name="create_project"),
    url(r'^chat/(?P<room_name>[^/]+)/$', views.room, name='room'),
]
