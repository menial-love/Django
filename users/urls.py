# encoding: utf-8
"""
@desc: 用户app路由
"""
from django.urls import path

from .views import UserRegister, UserLogin, UserLogout, UserHome, EditUserProfile, UserList

app_name = 'users'


urlpatterns = [
    path('register/', UserRegister.as_view(), name='user-register'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
    path('home/<int:user_id>/', UserHome.as_view(), name='user-home'),
    path('list/', UserList.as_view(), name='user-list'),
    path('edit/<int:user_id>/', EditUserProfile.as_view(), name='edit-profile'),
]