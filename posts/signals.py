# encoding: utf-8
"""
@desc: 帖子信号
"""

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post


@receiver(m2m_changed, sender=Post.like_users.through)
def post_like_users_changed(sender, instance, **kwargs):
    """
    当帖子喜欢数据发生变化时，更新其对应的人数
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.like_count = instance.like_users.count()
    instance.save()
