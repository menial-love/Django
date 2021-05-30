from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import View

from users.models import UserProfile
from users.forms import UserProfileForm


class UserRegister(View):
    """
    用户注册视图
    """
    def get(self, request):
        current_page = 'register'
        return render(request, 'users/register.html', {
            'current_page': current_page,
        })

    def post(self, request):
        # 判断是否是以ajax提交的
        if request.is_ajax():
            email = request.POST.get('email', None)
            password1 = request.POST.get('password1', None)
            password2 = request.POST.get('password2', None)
            # 确保前端提交的数据不为空
            if email and password1 and password2:
                # 切割邮箱，取@符号前面作为用户名
                username = email.split('@')[0]
                # 检查该邮箱是否被注册过
                if UserProfile.objects.filter(username=username).exists():
                    return JsonResponse({'msg': 'exists'})
                if not password1 == password2:
                    return JsonResponse({'msg': 'mismatch'})
                # 创建新的用户
                new_user = UserProfile(username=username, email=email)
                new_user.password = make_password(password2)
                new_user.save()
                return JsonResponse({'msg': 'ok'})
        return JsonResponse({'msg': 'ko'})


class CustomBackend(ModelBackend):
    """
    增加邮箱登录
    继承ModelBackend类，覆盖authenticate方法, 增加邮箱认证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 使用get是因为不希望用户存在两个, Q：使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # 判断密码是否匹配时，django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有check_password(self, raw_password)方法
            if user.check_password(password):
                return user
        except BaseException as e:
            print(e)
            return None


class UserLogin(View):
    """
    用户登录视图
    """
    def get(self, request):
        current_page = 'login'
        return render(request, 'users/login.html', {
            'current_page': current_page,
        })

    def post(self, request):
        if request.is_ajax():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            if username and password:
                user = authenticate(username=username, password=password)
                # 设置session的过期时间，这里参数0表示关闭浏览器session即过期
                request.session.set_expiry(0)
                if user is not None:
                    login(request, user) # login方法会将user放到request中，在前端可使用request.user
                    return JsonResponse({'msg': 'ok'})
        return JsonResponse({'msg': 'ko'})


class UserLogout(View):
    """
    用户退出登录
    """
    def get(self, request):
        logout(request)
        return JsonResponse({'msg': 'ok'})


class UserHome(View):
    """
    用户个人主页
    """
    def get(self, request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        posts = user.user_posts.all()
        reviews = user.user_reviews.all()
        replies = user.user_replies.all()
        current_page = "Home"
        return render(request, 'users/home.html', {
            'current_page': current_page,
            'user': user,
            'posts': posts,
            'reviews': reviews,
            'replies': replies
        })


class UserList(View):
    """
    用户列表
    """
    def get(self, request):
        users = UserProfile.objects.all()
        return render(request, 'users/all.html', {'users': users})


class EditUserProfile(LoginRequiredMixin, View):
    """
    LoginRequiredMixin类
    编辑用户资料
    """
    def get(self, request, user_id):
        user = self.get_user(request, user_id)
        form = UserProfileForm(instance=user)
        return render(request, 'users/profile.html', {
            'user': user,
            'form': form,
        })

    def post(self, request, user_id):
        user = self.get_user(request, user_id)
        form = UserProfileForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(user.get_absolute_url())
        return render(request, 'users/profile.html', {
            'user': user,
            'form': form,
            'msg': 'ko'
        })

    @staticmethod
    def get_user(request, user_id):
        user = get_object_or_404(UserProfile, id=int(user_id))
        check_is_request_owner(request, user)
        return user


def check_is_request_owner(request, owner):
    """
    检查是当前请求者是为所有者
    :param request:
    :param owner:
    :return: 引发Http404
    """
    if request.user != owner:
        raise Http404


