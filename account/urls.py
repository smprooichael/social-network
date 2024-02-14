from django.urls import path
from .views import UserRegestration, UserLogin, UserLogout

app_name = 'account'
urlpatterns = [
    path('register/', UserRegestration.as_view(), name='user_register'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('logout/', UserLogout.as_view(), name='user_logout'),
]