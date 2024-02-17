from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm
from django.utils.text import slugify

class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, 'home/detail.html', {'post':post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk = post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'The post is deleted successfully', 'success')
            return redirect('home:home')
        else:
            messages.error(request, "You can't delete this post", "danger")


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    template_name = 'home/update.html'

    def setup(self, request, *args, **kwargs):
        self.post_instrance = Post.objects.get(pk = kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.id == self.post_instrance.user.id:
            messages.error(request, 'You can\'t update this post', 'warning')
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, post_id):
        form = self.form_class(instance=self.post_instrance)
        return render(request, self.template_name, {'form':form})

    def post(self, request, post_id):
        form = self.form_class(request.POST, instance=self.post_instrance)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(new_post.body[:30])
            new_post.save()
            messages.success(request, 'The post updated successfully', 'success')
            return redirect('home:post_detail', self.post_instrance.id, self.post_instrance.slug)
        return render(request, self.template_name, {'form':form})
