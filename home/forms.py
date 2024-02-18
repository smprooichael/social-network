from django.forms import ModelForm
from .models import Post


class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']