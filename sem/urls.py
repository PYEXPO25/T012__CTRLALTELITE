from django.urls import path
from .views import (
    home, user_login, user_logout, register, api_login, protected_view,
    login_view, register_view, create_account, forget_password
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('api/register/', register, name='api_register'),  # API Registration
    path('api/login/', api_login, name='api_login'),
    path('protected/', protected_view, name='protected_view'),
    path('login-page/', login_view, name='login_page'),
    path('register-page/', register_view, name='register_page'),
    path('createaccount/', create_account, name='create_account'),
    path('forget/', forget_password, name='forget_password'),
]
