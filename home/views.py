from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetail(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, 'home/detail.html', {'post':post})


class PostDelete(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk = post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'The post is deleted successfully', 'success')
            return redirect('home:home')
        else:
            messages.error(request, "You can't delete this post", "danger")