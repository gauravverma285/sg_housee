from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_view
from . import api
from rest_framework.routers import DefaultRouter


from accounts import api as account

router = DefaultRouter()
router.register("add-client/(?P<id>\d+)", api.Addclient),

urlpatterns = [
    # Auth APIs
    path('signup_api/', api.SignupApiView.as_view(), name='signup-api'),
    path('login/', api.LoginApiView.as_view(), name='login'),
    path('reset-password/', api.ResetPasswordApiView.as_view(), name='reset-password-api'),
    path('user-forgot-password/', api.ForgotPasswordApiView.as_view(),
         name='forgot-password-api'),
    path('forgot-reset-password-api/', api.ForgotResetPasswordApiView.as_view(),
         name='forgot-reset-password-api'),
]

urlpatterns=router.urls