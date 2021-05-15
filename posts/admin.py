from django.contrib import admin
from .models import Post, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """
    板块后台管理
    """
    list_display = ['id', 'title', 'user']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    帖子后台管理
    """
    list_display = ['id', 'title', 'user', 'created']
