# encoding: utf-8
"""
@desc: 用户模板标签
"""

from django import template

from ..models import UserProfile

register = template.Library()


@register.simple_tag
def get_online_users(count=8):
    """
    获取在线用户
    :param count: 默认用户数量
    :return:
    """
    return UserProfile.objects.all()[:count]
