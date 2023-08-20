from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path(
        'users/set-password/',
        views.UserSetPasswordView.as_view(),
        name='user-set-password',
    ),
    path(
        'users/reset-password/',
        views.ResetPasswordView.as_view(),
        name='user-reset-password',
    ),
    path(
        'users/reset-password-confirm/',
        views.ResetPasswordConfirmView.as_view(),
        name='user-reset-password-confirm',
    ),
    path(
        'users/activate/<uid>/<token>',
        views.UserActivateView.as_view(),
        name='user-activate',
    ),
    path(
        'users/request-activation-email/',
        views.UserRequestActivationEmailView.as_view(),
        name='user-request-activation-email',
    ),
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
