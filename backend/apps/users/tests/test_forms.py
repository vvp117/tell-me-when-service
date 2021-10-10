from django.test import TestCase

from apps.users.models import User
from apps.users.forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
)


STRONG_PWD = r'Qwerty123!'


class UserRegisterFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password=STRONG_PWD,
        )

    def test_form_fields(self):
        form = UserRegisterForm()

        self.assertListEqual(
            list(form.fields.keys()),
            ['username', 'email', 'password1', 'password2']
        )

    def test_email_help_text(self):
        form = UserRegisterForm()

        self.assertEquals(
            form.fields['email'].help_text,
            'Required. Your e-mail, please...'
        )

    def test_email_already_in_use(self):
        form_data = {
            'username': 'user2',
            'email': 'user1@gmail.com',  # already in use
            'password1': STRONG_PWD,
            'password2': STRONG_PWD,
        }
        form = UserRegisterForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertIn('email', form.errors)


class UserUpdateFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password=STRONG_PWD,
        )
        User.objects.create_user(
            username='user2',
            email='user2@gmail.com',
            password=STRONG_PWD,
        )

    def test_form_fields(self):
        form = UserUpdateForm()

        self.assertListEqual(
            list(form.fields.keys()),
            ['username', 'email']
        )

    def test_email_already_in_use(self):
        user1 = User.objects.get(id=1)
        form_data = {
            'username': 'user1',
            'email': 'user2@gmail.com',  # already in use
        }
        form = UserUpdateForm(instance=user1, data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertIn('email', form.errors)


class ProfileUpdateFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password=STRONG_PWD,
        )

    def test_form_fields(self):
        form = ProfileUpdateForm()

        self.assertListEqual(
            list(form.fields.keys()),
            ['image']
        )
