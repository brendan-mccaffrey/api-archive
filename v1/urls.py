from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registration_view, name='register'),
    path('login/', obtain_auth_token, name='login'),
]