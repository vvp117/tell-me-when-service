from django.test import TestCase, Client
from django.urls import reverse
from django.forms import BaseForm
from django.contrib.auth.models import User

from main.tests.utils import SimpleUploadedImage


class RegistrationTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.url_register = reverse('users-register')
        self.url_login = reverse('users-login')
        self.url_logout = reverse('users-logout')

        self.reg_post_cases = {
            'success': {
                    'username': 'user1',
                    'email': 'user1@gmail.com',
                    'password1': r'Qwerty123!',
                    'password2': r'Qwerty123!',
                },
            'incorrect-email': {
                    'username': 'user1',
                    'email': 'user1_gmail.com',
                    'password1': r'Qwerty123!',
                    'password2': r'Qwerty123!',
                },
            'passwords-not-match': {
                    'username': 'user1',
                    'email': 'user1@gmail.com',
                    'password1': r'Qwerty123!',
                    'password2': r'Qwerty12!',
                },
            'password-is-simple': {
                    'username': 'user1',
                    'email': 'user1@gmail.com',
                    'password1': r'123',
                    'password2': r'123',
                },
        }


class RegistrationTestViews(RegistrationTestCase):

    def test_register_get(self):
        response = self.client.get(self.url_register)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_success(self):
        reg_data = self.reg_post_cases['success']

        response = self.client.post(self.url_register, reg_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.url_login)

        query_set = User.objects.filter(username=reg_data['username'])
        self.assertEqual(query_set.count(), 1)

    def test_register_passwords_not_match(self):
        reg_data = self.reg_post_cases['passwords-not-match']
        response = self.client.post(self.url_register, reg_data)

        self.assertEquals(response.status_code, 200, msg=reg_data)
        self.assertIn('form', response.context)

        form: BaseForm = response.context['form']

        self.assertTrue(form.has_error('password2', 'password_mismatch'),
                        msg=reg_data)

    def test_register_password_is_simple(self):
        reg_data = self.reg_post_cases['password-is-simple']
        response = self.client.post(self.url_register, reg_data)

        self.assertEquals(response.status_code, 200, msg=reg_data)
        self.assertIn('form', response.context)

        form: BaseForm = response.context['form']

        error_codes = [
            'password_too_short',
            'password_too_common',
            'password_entirely_numeric',
        ]
        for error_code in error_codes:
            self.assertTrue(form.has_error('password2', error_code), reg_data)

    def test_register_incorrect_email(self):
        reg_data = self.reg_post_cases['incorrect-email']
        response = self.client.post(self.url_register, reg_data)

        self.assertEquals(response.status_code, 200, msg=reg_data)
        self.assertIn('form', response.context)

        form: BaseForm = response.context['form']

        self.assertTrue(form.has_error('email', 'invalid'),
                        msg=reg_data)

    def test_username_already_exists(self):
        reg_data = self.reg_post_cases['success']
        User.objects.create(
            username=reg_data['username'],
            email=reg_data['email'],
            password=reg_data['password1'],
        )

        response = self.client.post(self.url_register, reg_data)

        self.assertEquals(response.status_code, 200, msg=reg_data)
        self.assertIn('form', response.context)

        form: BaseForm = response.context['form']

        self.assertTrue(form.has_error('username', 'unique'),
                        msg=reg_data)


class LoginTestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.url_login = reverse('users-login')
        self.url_homepage = reverse('main-index')

        self.user_data = {
            'username': 'user1',
            'email': 'user1@gmail.com',
            'password': r'Qwerty123!',
        }

        self.user: User = User.objects.create_user(**self.user_data)

    def test_login_page(self):
        response = self.client.get(self.url_login)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_success_redirect(self):
        response = self.client.post(self.url_login, self.user_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.url_homepage)


class ProfileTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.url_profile = reverse('users-profile')
        self.url_login = reverse('users-login')
        self.url_logout = reverse('users-logout')

        self.user1_data = {
            'username': 'user1',
            'email': 'user1@gmail.com',
            'password': r'Qwerty123!',
        }
        self.user2_data = {
            'username': 'user2',
            'email': 'user2@gmail.com',
            'password': r'Qwerty123!',
        }

        self.user1: User = User.objects.create_user(**self.user1_data)
        self.user2: User = User.objects.create_user(**self.user2_data)


class ProfileTestViews(ProfileTestCase):

    def test_profile_without_login(self):
        response = self.client.get(self.url_profile)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,
                             f'{self.url_login}?next={self.url_profile}')

    def test_profile_after_login(self):
        self.client.login(**self.user1_data)

        response = self.client.get(self.url_profile)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_set_username_without_login(self):
        response = self.client.post(self.url_profile, {'username': 'user2'})

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,
                             f'{self.url_login}?next={self.url_profile}')

    def test_set_username_after_login(self):
        self.client.login(**self.user1_data)

        user_data = self.user1_data.copy()
        user_data['username'] = 'user11'

        response = self.client.post(self.url_profile, user_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.url_profile)

    def test_set_non_unique_username(self):
        self.client.login(**self.user1_data)

        user_data = self.user1_data.copy()
        user_data['username'] = self.user2_data['username']
        response = self.client.post(self.url_profile, user_data)

        self.assertEquals(response.status_code, 200)
        self.assertIn('form', response.context)

        form: BaseForm = response.context['form']

        self.assertTrue(form.has_error('username', 'unique'))

    def test_set_non_unique_email(self):
        self.client.login(**self.user1_data)

        user_data = self.user1_data.copy()
        user_data['email'] = self.user2_data['email']
        response = self.client.post(self.url_profile, user_data)

        self.assertEquals(response.status_code, 200)
        self.assertIn('form', response.context)

        form: BaseForm = response.context['form']

        self.assertTrue(form.has_error('email', 'unique'))

    def test_update_profile_image(self):
        self.client.login(**self.user1_data)

        user_data = self.user1_data.copy()
        user_data['image'] = SimpleUploadedImage('my-image.jpg',
                                                 height=1024,
                                                 width=1024,
                                                 color=(255, 0, 0))

        response = self.client.post(self.url_profile, user_data)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.url_profile)
