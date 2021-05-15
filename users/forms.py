# encoding: utf-8
"""
@desc: 
"""
from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    修改个人信息
    """
    class Meta:
        model = UserProfile
        fields = ('avatar', 'nickname', 'signature')
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control border-0 pl-0'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control bg-light'}),
            'signature': forms.TextInput(attrs={'class': 'form-control bg-light'}),
        }
