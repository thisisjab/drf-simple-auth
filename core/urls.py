from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


urlpatterns = [
    path('users/', views.UserCreateView.as_view(), name='user-create'),
    path(
        'users/activate/<uid>/<token>',
        views.UserActivateView.as_view(),
        name='user-activate',
    ),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
