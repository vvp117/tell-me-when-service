from django.test import TestCase
from django.db import models
from django.db.utils import IntegrityError

from apps.users.models import User
from apps.devices.models import Device


class DeviceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password=r'Qwerty123!',
        )
        Device.objects.create(
            name='device1',
            description='my device',
            owner=user1,
        )

    def test_field_props(self):
        device = Device.objects.get(pk=1)
        get_field = device._meta.get_field

        name_field = get_field('name')
        self.assertEquals(name_field.max_length, 150)

        create_date_field = get_field('create_date')
        self.assertEquals(create_date_field.auto_now_add, True)

        modified_date_field = get_field('modified_date')
        self.assertEquals(modified_date_field.auto_now, True)

        owner_field = get_field('owner')
        self.assertEquals(owner_field.db_constraint, True)
        self.assertEquals(owner_field.many_to_one, True)
        self.assertEquals(owner_field.null, False)
        self.assertEquals(owner_field.remote_field.on_delete, models.CASCADE)

    def test_try_create_device_without_owner(self):
        with self.assertRaisesMessage(
                IntegrityError,
                'NOT NULL constraint failed: devices_device.owner_id'):
            Device.objects.create(name='device1')

    def test_cascade_delete_device(self):
        user1 = User.objects.get(id=1)
        user1.delete()
        device_exists = Device.objects.filter(owner=1).exists()

        self.assertFalse(device_exists)

    def test_device_to_str(self):
        device = Device.objects.get(pk=1)
        device_as_str = f'{device.name} ({device.id})'

        self.assertEquals(str(device), device_as_str)

    def test_get_absolute_url(self):
        device = Device.objects.get(pk=1)

        self.assertEquals(device.get_absolute_url(), '/devices/1/')
