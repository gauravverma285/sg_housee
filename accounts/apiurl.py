from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_view
from . import api

from accounts import api as account

urlpatterns = [
    # Auth APIs
    path('signup_api/', api.SignupApiView.as_view(), name='signup-api'),
]