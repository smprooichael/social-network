from django.urls import path
from .views import HomeView, PostDetail

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('detail/<int:post_id>/<slug:post_slug>', PostDetail.as_view(), name='post_detail'),
]