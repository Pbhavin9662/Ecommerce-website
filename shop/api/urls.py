from django.urls import path
from shop.views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [

    path('login/', ObtainAuthTokenView, name="login"),
    path('register/', registration_view, name="register"),
]
