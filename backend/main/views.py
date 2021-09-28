from django.shortcuts import render, redirect

from .timezones import get_timezones


def home(request):
    return render(request, 'main/index.html')


def timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'main/timezone.html', {'timezones': get_timezones()})


def about(request):
    return render(request, 'main/about.html')
