from django.contrib import admin

from .models import Review, Reply


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    后台评论管理
    """
    list_display = ['id', 'post', 'content', 'user', 'created']


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    """
    后台评论管理
    """
    list_display = ['id', 'review', 'content', 'user', 'created']
