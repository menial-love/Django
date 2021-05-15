from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from posts.models import Post

from .models import Review, Reply


class ReviewDetail(View):
    """
    评论详情
    """
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=int(review_id))
        replies = review.get_reply_list()
        return render(request, 'reviews/review-detail.html', {
            'review': review,
            'replies': replies,
        })


class AddReview(LoginRequiredMixin, View):
    """
    添加回复
    """
    def post(self, request):
        post_id = request.POST.get('postId', None)
        reply_text = request.POST.get('text', None)

        if request.is_ajax() and post_id and reply_text:
            try:
                post = Post.objects.get(id=int(post_id))
                new_review = Review(content=reply_text, post=post)
                new_review.user = request.user
                new_review.save()
                return JsonResponse({'msg': 'ok'})
            except BaseException as e:
                print(e)
                return JsonResponse({'msg': 'ko'})
        return JsonResponse({'msg': 'ko'})


class AddReply(LoginRequiredMixin, View):
    """
    添加回复
    """
    def post(self, request):
        review_id = request.POST.get('rid', None)
        parent_id = request.POST.get('pid', None)
        reply_text = request.POST.get('text', None)

        if request.is_ajax() and review_id and reply_text:
            try:
                review = Review.objects.get(id=int(review_id))
                parent = Reply.objects.get(id=int(parent_id)) if int(parent_id) != 0 else None
                new_reply = Reply(content=reply_text, review=review, parent=parent)
                new_reply.user = request.user
                new_reply.save()
                return JsonResponse({'msg': 'ok'})
            except BaseException as e:
                print(e)
                return JsonResponse({'msg': 'ko'})

        return JsonResponse({'msg': 'ko'})


class AddLike(LoginRequiredMixin, View):
    """
    点赞评论或回复
    """
    def post(self, request):
        rid = request.POST.get('rid', None)
        action = request.POST.get('action', None)
        ctg = request.POST.get('ctg', None)
        msg = 'ko'
        if request.is_ajax() and rid and action and ctg:
            if ctg == 'review':
                msg = self.like_review(request, rid, action)
            elif ctg == 'reply':
                msg = self.like_reply(request, rid, action)
        return JsonResponse({'msg': msg})

    @staticmethod
    def like_review(request, rid, action):
        try:
            review = Review.objects.get(id=int(rid))
            if action == 'like':
                review.like_users.add(request.user)
            else:
                review.like_users.remove(request.user)
            return 'ok'
        except Review.DoesNotExist:
            return 'ko'

    @staticmethod
    def like_reply(request, rid, action):
        try:
            reply = Reply.objects.get(id=int(rid))
            if action == 'like':
                reply.like_users.add(request.user)
            else:
                reply.like_users.remove(request.user)
            return 'ok'
        except Reply.DoesNotExist:
            return 'ko'




