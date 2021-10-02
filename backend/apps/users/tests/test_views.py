from django.test import TestCase, Client
from django.urls import reverse
from django.forms import BaseForm
from django.contrib.auth.models import User


class RegistrationTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.url_register = reverse('users-register')
        self.url_profile = reverse('users-profile')
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
