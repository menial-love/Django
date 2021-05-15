from django.db import models
from django.conf import settings
from django.urls import reverse

from posts.models import Post


class Review(models.Model):
    """
    评论表
    """
    content = models.TextField(verbose_name='内容')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='post_reviews',
                             verbose_name='所属帖子')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_reviews',
                             verbose_name='用户')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                        related_name='like_reviews',
                                        verbose_name='点赞的用户')
    like_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ('-created',)
        
    def get_absolute_url(self):
        """
        获取评论绝对路径
        :return:
        """
        return reverse('reviews:review-detail', args=[self.pk])

    def get_reply_list(self):
        """
        获取评论列表
        :return:
        """
        return self.review_replies.all()

    def get_reply_count(self):
        """
        获取评回复评数
        :return:
        """
        return self.review_replies.count()

    def __str__(self):
        return self.content


class Reply(models.Model):
    """
    回复表
    """
    content = models.TextField(verbose_name='内容')
    review = models.ForeignKey('Review', on_delete=models.CASCADE,
                               related_name='review_replies',
                               verbose_name='评论')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_replies',
                             verbose_name='用户')
    # 创建父亲节点用户构建多级评论
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               blank=True, null=True, related_name='children')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                        related_name='like_reply',
                                        verbose_name='点赞的用户')
    like_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = verbose_name
        ordering = ('-created',)

    def __str__(self):
        return self.content


