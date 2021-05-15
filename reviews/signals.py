# encoding: utf-8
"""
@desc: 评论模块信号
"""

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Review, Reply


@receiver(m2m_changed, sender=Review.like_users.through)
def review_like_users_changed(sender, instance, **kwargs):
    """
    当评论喜欢数据发送变化时，更新其对应的人数
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.like_count = instance.like_users.count()
    instance.save()


@receiver(m2m_changed, sender=Reply.like_users.through)
def reply_like_users_changed(sender, instance, **kwargs):
    """
    当回复喜欢数据发送变化时，更新其对应的人数
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.like_count = instance.like_users.count()
    instance.save()
