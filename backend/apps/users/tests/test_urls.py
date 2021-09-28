from uuid import uuid4

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from apps.users import views


class TestUrls(SimpleTestCase):

    def test_register_resolved(self):
        url = reverse('users-register')
        self.assertEquals(resolve(url).func, views.register)

    def test_profile_resolved(self):
        url = reverse('users-profile')
        self.assertEquals(resolve(url).func, views.profile)

    def test_login_resolved(self):
        url = reverse('users-login')
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_resolved(self):
        url = reverse('users-logout')
        self.assertEquals(resolve(url).func.view_class, auth_views.LogoutView)

    def test_password_reset_resolved(self):
        url = reverse('password_reset')
        self.assertEquals(resolve(url).func.view_class,
                          auth_views.PasswordResetView)

    def test_password_reset_done_resolved(self):
        url = reverse('password_reset_done')
        self.assertEquals(resolve(url).func.view_class,
                          auth_views.PasswordResetDoneView)

    def test_password_reset_confirm_resolved(self):
        url = reverse('password_reset_confirm', args=['MQ', str(uuid4())])
        self.assertEquals(resolve(url).func.view_class,
                          auth_views.PasswordResetConfirmView)

    def test_password_reset_complete_resolved(self):
        url = reverse('password_reset_complete')
        self.assertEquals(resolve(url).func.view_class,
                          auth_views.PasswordResetCompleteView)
