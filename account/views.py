from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterForm, UserLoginForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relations, Profile

class UserRegestration(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You logged in', 'warning')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            messages.success(request, 'You registered successfully!', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserLogin(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You logged in ', 'warning')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You logged in', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'Username or password is wrong', 'warning')
        return render(request, self.template_name, {'form':form})

class UserLogout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out successfully', 'success')
        return redirect('home:home')


class UserProfile(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk = user_id)
        posts = user.posts.filter()
        relation = Relations.objects.filter(from_user = request.user, to_user = user)
        if relation.exists():
            is_following = True
        return render(request, 'account/profile.html', {'user': user, 'posts': posts, 'is_following': is_following})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk = user_id)
        relation = Relations.objects.filter(from_user = request.user, to_user =user)
        if relation.exists():
            messages.error(request, 'You already follow this user', 'warning')
            return redirect('account:user_profile', user.id)
        else:
            Relations(from_user=request.user, to_user=user).save()
            messages.success(request, 'You followed this user', 'success')
            return redirect('account:user_profile', user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk = user_id)
        relation = Relations.objects.filter(from_user = request.user, to_user =user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'You unfollowed this user', 'success')
            return redirect('account:user_profile', user.id)
        else:
            messages.error(request, "You haven't followed this user yet", 'warning')
            return redirect('account:user_profile', user.id)


class UserEditProfile(LoginRequiredMixin, View):
    form_class = EditProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'email':request.user.email})
        return render(request, 'account/edit_profile.html', {'form':form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile, initial={'email':request.user.email})
        if form.is_valid():
            user = form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'You profile changed successfully', 'success')
        return redirect('account:user_profile',  request.user.id)
