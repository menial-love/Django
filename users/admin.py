from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    用户后台管理，is_staff：是否管理员
    """
    list_display = ['id', 'username', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active']



