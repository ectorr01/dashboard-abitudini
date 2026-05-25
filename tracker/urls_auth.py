from django.urls import path
from . import views_auth

urlpatterns = [
    path('', views_auth.registrazione, name='registrazione'),
]