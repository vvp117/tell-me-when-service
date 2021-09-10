from django.shortcuts import render


devices = [
    {
        'id': 1,
        'name': 'filter 1',
        'descr': 'water filter',
        'type': 'filter'
    },
    {
        'id': 2,
        'name': 'electric shaver Bosh',
        'descr': 'self-cleaning shaver',
        'type': 'shaver'
    },
    {
        'id': 3,
        'name': 'coffee machine Delongi',
        'descr': 'coffee machine on cooking',
        'type': 'coffee-machine'
    }
]


def devices_list(request):
    context = {
        'title': 'Devices',
        'devices': devices
    }
    return render(request, 'devices/index.html', context)
