from django.shortcuts import render
from django.contrib.auth.mixins import (
    LoginRequiredMixin as LoginReq,
    UserPassesTestMixin as UserPass,
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Device


def devices_list(request):
    context = {
        'title': 'Devices',
        'devices': Device.objects.all()
    }
    return render(request, 'devices/index.html', context)


def check_owner(view):
    device = view.get_object()
    return device.owner == view.request.user


class DeviceListView(LoginReq, ListView):
    model = Device
    template_name = 'devices/index.html'  # <app/<model>_<viewtype>.html
    context_object_name = 'devices'
    # ordering = ['-create_date']

    def get_queryset(self):
        return Device.objects.filter(
            owner=self.request.user
        ).order_by('-create_date')


class DeviceDetailView(LoginReq, UserPass, DetailView):
    model = Device

    def test_func(self):
        return check_owner(self)


class DeviceCreateView(LoginReq, CreateView):
    model = Device
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DeviceUpdateView(LoginReq, UserPass, UpdateView):
    model = Device
    fields = ['name', 'description']

    def test_func(self):
        return check_owner(self)


class DeviceDeleteView(LoginReq, UserPass, DeleteView):
    model = Device
    success_url = '/devices/'

    def test_func(self):
        return check_owner(self)
