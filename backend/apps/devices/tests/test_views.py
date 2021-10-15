from uuid import uuid4

from django.test import TestCase, Client
from django.urls import reverse
# from django.forms import BaseForm
from django.contrib.auth.models import User

from apps.devices.models import Device
from main.tests.utils import strong_password


class DeviceViewsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1_data = {
            'username': 'user1',
            'email': 'user1@gmail.com',
            'password': strong_password(10),
        }
        cls.user2_data = {
            'username': 'user2',
            'email': 'user2@gmail.com',
            'password': strong_password(10),
        }

        user1 = User.objects.create_user(**cls.user1_data)
        user2 = User.objects.create_user(**cls.user2_data)

        Device.objects.create(
            name='device1 of user1',
            owner=user1,
        )
        Device.objects.create(
            name='device2 of user2',
            owner=user2,
        )

        #  Total: 16 devices for user1
        for i in range(15):
            Device.objects.create(
                name=f'device{i} of user1',
                owner=user1,
            )

    def setUp(self):
        self.client = Client()

        self.url_login = reverse('users-login')
        self.url_devices = reverse('devices-list')
        self.url_device_new = reverse('devices-new')

        self.paginate_by = 5

        self.user1: User = User.objects.get(id=1)
        self.user2: User = User.objects.get(id=2)

        self.device_user1: Device = Device.objects.get(id=1, owner=1)
        self.device_user2: Device = Device.objects.get(id=2, owner=2)

        self.url_device_user1 = reverse('devices-item', args=[1])
        self.url_device_user2 = reverse('devices-item', args=[2])


class DeviceListTestViews(DeviceViewsTestCase):

    def test_devices_without_login(self):
        response = self.client.get(self.url_devices)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,
                             f'{self.url_login}?next={self.url_devices}')

    def test_devices_after_login(self):
        self.client.login(**self.user1_data)

        response = self.client.get(self.url_devices)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'devices/device_list.html')

    def test_curent_owner_devices_only(self):
        self.client.login(**self.user2_data)

        response = self.client.get(self.url_devices)

        self.assertEquals(response.status_code, 200)
        self.assertIn('devices', response.context)

        for device in response.context['devices']:
            self.assertEquals(device.owner, self.user2)

    def test_devices_pagination(self):
        self.client.login(**self.user1_data)

        response = self.client.get(self.url_devices)

        self.assertEquals(response.status_code, 200)
        self.assertIn('devices', response.context)

        self.assertIn('is_paginated', response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEquals(len(response.context['devices']), self.paginate_by)

    def test_last_page_devices(self):
        self.client.login(**self.user1_data)

        total_devices = Device.objects.filter(owner=self.user1).count()
        last_devices = total_devices % self.paginate_by
        last_page = (total_devices // self.paginate_by + bool(last_devices))

        response = self.client.get(self.url_devices, {'page': last_page})

        self.assertEquals(response.status_code, 200)
        self.assertIn('devices', response.context)

        self.assertIn('is_paginated', response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEquals(len(response.context['devices']), last_devices)


class DeviceDetailTestViews(DeviceViewsTestCase):

    def test_device_without_login(self):
        response = self.client.get(self.url_device_user1)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,
                             f'{self.url_login}?next={self.url_device_user1}')

    def test_device_after_login(self):
        self.client.login(**self.user1_data)

        response = self.client.get(self.url_device_user1)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'devices/device_detail.html')

    def test_curent_owner_device_only(self):
        self.client.login(**self.user1_data)

        response = self.client.get(self.url_device_user2)

        self.assertEquals(response.status_code, 403)


class DeviceCreateTestViews(DeviceViewsTestCase):

    def test_new_device_without_login(self):
        response = self.client.get(self.url_device_new)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,
                             f'{self.url_login}?next={self.url_device_new}')

    def test_new_device_after_login(self):
        self.client.login(**self.user1_data)

        response = self.client.get(self.url_device_new)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'devices/device_form.html')

    def test_create_device_success(self):
        self.client.login(**self.user1_data)

        device_name = str(uuid4())
        device_data = {
            'name': device_name,
            'description': 'my device',
        }

        response = self.client.post(self.url_device_new, device_data)

        query_set = Device.objects.filter(name=device_name)
        self.assertTrue(query_set.exists())

        # Device created
        new_device = query_set.first()
        url_new_device = reverse('devices-item', args=[new_device.pk])

        # Saved data correct
        self.assertEquals(new_device.owner, self.user1)
        self.assertEquals(new_device.description, device_data['description'])

        # Redirect correct
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, url_new_device)

        response = self.client.get(url_new_device)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'devices/device_detail.html')
