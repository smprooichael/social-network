from django.shortcuts import render
from django.views import View
from .forms import UserRegisterForm

class UserRegestration(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'account/register.html', {'form': form})