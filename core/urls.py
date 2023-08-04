from django.urls import path

from . import views


urlpatterns = [
    path('users/', views.UserCreateView.as_view(), name='user-create'),
    path(
        'users/activate/<uid>/<token>',
        views.UserActivateView.as_view(),
        name='user-activate',
    ),
]
