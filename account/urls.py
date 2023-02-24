from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import logout

urlpatterns = [
    path('login/', views.hehe_login, name='login'),
    path('logout/', views.hehe_logout, name='logout'),
    path('signup/', views.register, name='register'),
]