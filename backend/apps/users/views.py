from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm


def register(request: WSGIRequest):
    if request.POST:
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request,
                f'Your account has been created!'
                ' You are now able to log in...')

            return redirect('users-login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request: WSGIRequest):
    return render(request, 'users/profile.html')
