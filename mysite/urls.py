"""
URL configuration for SEM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import (
    home, user_login, user_logout, register, api_login, protected_view,
    login_view, register_view, create_account, forget_password  # Ensure these are imported
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
