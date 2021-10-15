from django.test import SimpleTestCase
from django.urls import reverse, resolve

from apps.devices import views


class TestUrls(SimpleTestCase):

    def test_device_list_resolved(self):
        url = reverse('devices-list')
        self.assertEquals(resolve(url).func.view_class,
                          views.DeviceListView)

    def test_device_item_resolved(self):
        url = reverse('devices-item', args=['1'])
        self.assertEquals(resolve(url).func.view_class,
                          views.DeviceDetailView)

    def test_device_new_resolved(self):
        url = reverse('devices-new')
        self.assertEquals(resolve(url).func.view_class,
                          views.DeviceCreateView)

    def test_device_item_edit_resolved(self):
        url = reverse('devices-edit', args=['1'])
        self.assertEquals(resolve(url).func.view_class,
                          views.DeviceUpdateView)

    def test_device_item_del_resolved(self):
        url = reverse('devices-del', args=['1'])
        self.assertEquals(resolve(url).func.view_class,
                          views.DeviceDeleteView)
