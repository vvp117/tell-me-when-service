from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('register/', views.register, name='users-register'),
    path('profile/', views.profile, name='users-profile'),

    path('login/',
         auth_views.LoginView.as_view(
              template_name='users/login.html'),
         name='users-login'),
    path('logout/',
         auth_views.LogoutView.as_view(
              template_name='users/logout.html'),
         name='users-logout'),

    path('pwd-reset/',
         auth_views.PasswordResetView.as_view(
              template_name='users/pwd_reset.html'),
         name='password_reset'),
    path('pwd-reset-done',
         auth_views.PasswordResetDoneView.as_view(
              template_name='users/pwd_reset_done.html'),
         name='password_reset_done'),
    path('pwd-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
              template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('pwd-reset-complete',
         auth_views.PasswordResetCompleteView.as_view(
              template_name='users/pwd_reset_complete.html'),
         name='password_reset_complete'),
]
