from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
)


def register(request: WSGIRequest):
    if request.POST:
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your account has been created!'
                ' You are now able to log in...')

            return redirect('users-login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request: WSGIRequest):
    if request.POST:
        user_form = UserUpdateForm(request.POST,
                                   instance=request.user)
        prof_form = ProfileUpdateForm(request.POST,
                                      request.FILES,
                                      instance=request.user.profile)

        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()

            messages.success(request, 'Profile updated!')

            return redirect('users-profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        prof_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html',
                  context={'user_form': user_form, 'prof_form': prof_form})
