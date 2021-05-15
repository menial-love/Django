# encoding: utf-8
"""
@desc: 评论模块模板标签
"""

from django import template

from ..models import Reply, Review


register = template.Library()


@register.simple_tag
def check_is_like_review(rid, user):
    """
    检查是否已经点赞评论
    :param rid:
    :param user:
    :return:
    """
    return Review.objects.filter(id=rid, like_users=user).exists() if user.is_authenticated else False


@register.simple_tag
def check_is_like_reply(rid, user):
    """
    检查是否已经点赞回复
    :param rid:
    :param user:
    :return:
    """
    return Reply.objects.filter(id=rid, like_users=user).exists() if user.is_authenticated else False

