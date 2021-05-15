# encoding: utf-8
"""
@desc: 帖子表单
"""

from django import forms

from .models import Post


# 使用Django forms.modelform组件
class PostForm(forms.ModelForm):
    class Meta:  # 这里 model fields widgets 是固定写法
        # https://www.cnblogs.com/open-yang/p/11223192.html
        model = Post  # 这个是已经创建的模型类
        fields = ['cover_image', 'topic', 'src_url', 'title', 'content', ]  # 模型类的属性
        widgets = {
            'cover_image': forms.FileInput(attrs={'class': 'form-control border-0 pl-0'}),
            'topic': forms.Select(attrs={'class': 'form-control bg-light'}),
            'src_url': forms.TextInput(attrs={'class': 'form-control bg-light'}),
            'title': forms.TextInput(attrs={'class': 'form-control bg-light'}),
            'content': forms.Textarea(attrs={'class': 'form-control bg-light'}),
        }
