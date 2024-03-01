from django.forms import ModelForm
from .models import Post


class PostCreateUpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']