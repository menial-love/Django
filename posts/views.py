import setuptools.command.saveopts
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Topic
from .forms import PostForm

from posts.models import Photo


class PostDetail(View):
    """
    帖子详情
    """
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=int(post_id))
        post.view_count += 1
        post.save()
        reviews = post.get_review_list()
        photos = post.post_photos.all()   # 查找帖子所有图片传递给模板
        return render(request, 'posts/detail.html', {
            'post': post,
            'photos': photos,
            'reviews': reviews
        })


class LikePost(LoginRequiredMixin, View):
    """
    点赞帖子
    """
    def post(self, request):
        post_id = request.POST.get('postId', None)
        action = request.POST.get('action', None)
        if request.is_ajax() and post_id and action:
            try:
                post = Post.objects.get(id=int(post_id))
                if action == 'like':
                    post.like_users.add(request.user)
                else:
                    post.like_users.remove(request.user)
                return JsonResponse({'msg': 'ok'})
            except Post.DoesNotExist:
                return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class AddPost(LoginRequiredMixin, View):
    """
    发布帖子
    """
    def get(self, request):
        form = PostForm()
        return render(request, 'posts/add.html', {'form': form})

    def post(self, request):
        form = PostForm(data=request.POST, files=request.FILES)
        files = request.FILES.getlist("post_img_files")
        if form.is_valid():
            try:
                # 以下三行将帖子数据保存到数据库
                # https://blog.csdn.net/qq_21570029/article/details/79728458
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()

                for file in files:
                    media_url = "/media/image/post/content/" + file.name
                    new_photo = Photo(belong_post=new_post)
                    new_photo.absolute_url = media_url
                    new_photo.pic = file.name
                    new_photo.save()
                    destination = open('C:/F/python django bbs/bss_demo/media/image/post/content/' + file.name, 'wb+')
                    for chunk in file.chunks():
                        destination.write(chunk)
                    destination.close()

                # 发帖成功后页面重定向到用户个人主页
                return HttpResponseRedirect(request.user.get_absolute_url())
            except BaseException as e:
                print(e)
        return render(request, 'posts/add.html', {
            'form': form,
            'msg': 'ko'
        })


class DeletePost(View):
    """
    删除帖子
    """
    def post(self, request, post_id):

        post1 = get_object_or_404(Post, id=int(post_id))
        user = post1.user
        post1.delete()
        return HttpResponseRedirect(user.get_absolute_url())

class TopicDetail(View):
    """
    板块详情
    """
    # path('topic/detail/<int:topic_id>/', TopicDetail.as_view(), name='topic-detail'),
    # 在URL中用path方法使用<int>捕获url中的参数传递给视图函数
    # topic_id是url解析器捕获的参数丢给视图函数的
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, id=int(topic_id)) # 查询语句根据id查找板块名
        # 由于一个板块对应多个帖子属于一对多的关系，故在models.py中使用related_name
        # 在定义主表的外键的时候，给这个外键定义好一个名称
        # topic是板块
        posts = topic.topic_posts.order_by('-is_sticky')
        return render(request, 'posts/topic-detail.html', {
            'topic': topic,
            'posts': posts,  # 将这些参数放在字典中使用render函数传递给模板
            'topic_id': topic.id
        })


class StickyPost(LoginRequiredMixin, View):
    """
    顶置帖子(默认只有管理员可以顶置帖子）
    """
    def post(self, request):
        post_id = request.POST.get('pid', None)
        action = request.POST.get('action', None)

        if request.is_ajax() and post_id and action:
            try:
                post = get_object_or_404(Post, id=int(post_id))
                if action == 'sticky':
                    post.is_sticky = True
                else:
                    post.is_sticky = False
                post.save()
                return JsonResponse({'msg': 'ok'})
            except BaseException as e:
                print(e)
        return JsonResponse({'msg': 'ko'})
