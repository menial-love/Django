# encoding: utf-8
"""
@desc: 帖子路由
"""

from django.urls import path

from . import views
from .views import PostDetail, LikePost, AddPost, TopicDetail, StickyPost,DeletePost

app_name = 'posts'


urlpatterns = [
    path('detail/<int:post_id>/', PostDetail.as_view(), name='post-detail'),
    path('like/', LikePost.as_view(), name='like-post'),
    path('add/', AddPost.as_view(), name='add-post'),
    path('delete/<int:post_id>/', DeletePost.as_view(), name='post-delete'),
    # url中使用了as_view()方法后，返回的闭包会根据请求的方式到对应的视图函数中
    # 找以请求方式命名的函数进行执行。
    path('topic/detail/<int:topic_id>/', TopicDetail.as_view(), name='topic-detail'),
    path('sticky/', StickyPost.as_view()),
]