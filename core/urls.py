from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user-detail'),
    path(
        'users/activate/<uid>/<token>',
        views.UserActivateView.as_view(),
        name='user-activate',
    ),
    path(
        'users/send-activation-email/',
        views.UserSendActivationEmail.as_view(),
        name='user-send-activation-email',
    ),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
