from django.shortcuts import render
from .models import Device


def devices_list(request):
    context = {
        'title': 'Devices',
        'devices': Device.objects.all()
    }
    return render(request, 'devices/index.html', context)
