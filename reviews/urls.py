# encoding: utf-8
"""
@desc: 评论路由
"""

from django.urls import path

from .views import ReviewDetail, AddReply, AddLike, AddReview


app_name = 'reviews'

urlpatterns = [
    path('detail/<int:review_id>/', ReviewDetail.as_view(), name='review-detail'),
    path('add/review/', AddReview.as_view()),
    path('add/reply/', AddReply.as_view()),
    path('add/like/', AddLike.as_view()),
]