from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages

from .forms import UserRegisterForm


def register(request: WSGIRequest):
    if request.POST:
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect('main-index')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})
