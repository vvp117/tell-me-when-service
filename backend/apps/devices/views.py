from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
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
    FormView,
)

from .models import Device, DeviceImage
from .forms import DeviceImageEditForm


# def devices_list(request):
#     context = {
#         'title': 'Devices',
#         'devices': Device.objects.all()
#     }
#     return render(request, 'devices/device_list.html', context)


def check_owner(view):
    device = view.get_object()
    return device.owner == view.request.user


class DeviceListView(LoginReq, ListView):
    model = Device
    template_name = 'devices/device_list.html'  # <app/<model>_<viewtype>.html
    context_object_name = 'devices'
    paginate_by = 5
    # ordering = ['-create_date']

    def get_queryset(self):
        return Device.objects.filter(
            owner=self.request.user
        ).order_by('-create_date')


class DeviceDetailView(LoginReq, UserPass, DetailView):
    model = Device
    template_name = 'devices/device_detail.html'

    def get(self, request, *args, **kwargs):
        device = Device.objects.get(**kwargs)
        device_images = device.deviceimage_set.order_by('-create_date').all()
        return render(request, self.template_name,
                      {'device': device, 'device_images': device_images})

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


class DeviceImageView(LoginReq, UserPass, FormView):
    model = DeviceImage
    fields = ['image', 'description']
    template_name = 'devices/deviceimage_form.html'

    @property
    def device(self):
        return get_object_or_404(Device, pk=self.kwargs['device_pk'])

    @property
    def instance(self):
        pk = self.kwargs.get('pk')
        if pk:
            return get_object_or_404(DeviceImage, pk=pk)

    def get(self, request, *args, **kwargs):
        form = DeviceImageEditForm(
            instance=self.instance,
            initial={'device': self.device})

        return render(request, self.template_name,
                      {'form': form, 'device': self.device})

    def post(self, request, *args, **kwargs):
        form = DeviceImageEditForm(request.POST, request.FILES,
                                   instance=self.instance)
        if form.is_valid():
            form.save()
            return redirect('devices-item', self.device.pk)

        return render(request, self.template_name,
                      {'form': form, 'device': self.device})

    def test_func(self):
        return self.device.owner == self.request.user


class DeviceImageDeleteView(LoginReq, UserPass, DeleteView):
    model = DeviceImage

    def test_func(self):
        instance = self.get_object()
        return instance.device.owner == self.request.user

    def get_success_url(self):
        instance = self.get_object()
        return reverse('devices-item', kwargs={"pk": instance.device.pk})
