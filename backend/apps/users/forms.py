from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        help_text='Required. Your e-mail, please...'
        )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email):
            raise ValidationError(
                'Email "%(email)s" is already in use',
                code='unique',
                params={'email': email}
            )

        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exclude(id=self.instance.id):
            raise ValidationError(
                'Email "%(email)s" is already in use',
                code='unique',
                params={'email': email}
            )

        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
