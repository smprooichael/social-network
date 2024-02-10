from django.urls import path
from .views import UserRegestration

urlpatterns = [
    path('register/', UserRegestration.as_view(), name='user_register'),
]