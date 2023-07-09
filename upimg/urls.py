from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("home/", views.home, name='home'), 
    path("login/", views.user_login, name="login"),
    path("register/", views.user_register, name='register'), 
    path("logout/", views.user_logout, name="logout"),
    path("upload/", views.user_upload, name="upload"),
    path("home/<str:username>", views.user_images, name="user_home"),
    path("home/<str:username>/delete", views.user_delete, name='delete'),
]
