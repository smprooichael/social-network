from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        Comments = self.post_instance.pcomments.filter(is_reply=False)
        return render(request, 'home/detail.html', {'post':self.post_instance, 'Comments':Comments, 'form': self.form_class, 'form_reply': self.form_class_reply})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'Your comment submitted successfully!', 'success')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)



class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk = post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'The post is deleted successfully', 'success')
            return redirect('home:home')
        else:
            messages.error(request, "You can't delete this post", "danger")


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = 'home/update.html'

    def setup(self, request, *args, **kwargs):
        self.post_instrance = get_object_or_404(Post, pk = kwargs['post_id'])
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


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = 'home/create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'The post created successfully', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)


class ReplyCommentView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.reply = comment
            new_comment.is_reply = True
            new_comment.save()
            messages.success(request, 'Your reply submitted successfully.', 'success')
        return redirect('home:post_detail', post.id, post.slug)

