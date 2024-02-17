from django.urls import path
from .views import HomeView, PostDetail, PostDelete

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/detail/<int:post_id>/<slug:post_slug>', PostDetail.as_view(), name='post_detail'),
    path('post/delete/<int:post_id>/', PostDelete.as_view(), name='post_delete'),
]