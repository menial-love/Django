from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class UserProfile(AbstractUser):
    """
    用户表
    """
    nickname = models.CharField(max_length=32,
                                blank=True, null=True,
                                verbose_name='昵称')
    signature = models.CharField(max_length=128,
                                 blank=True, null=True,
                                 verbose_name='个性签名',
                                 default='这家伙很懒，什么都没有留下！')
    avatar = models.ImageField(upload_to='image/user/avatar', blank=True,
                               default='image/default_avatar.png', verbose_name='头像')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        """
        获取用户绝对路径
        :return:
        """
        # path('home/<int:user_id>/', UserHome.as_view(), name='user-home'),
        return reverse('users:user-home', args=[self.pk])

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username

