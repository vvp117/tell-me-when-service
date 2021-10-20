from django.test import TestCase
from django.db import models
from django.db.utils import IntegrityError

from apps.users.models import User
from apps.devices.models import Device, DeviceImage


class DeviceModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password=r'Qwerty123!',
        )
        cls.device1 = Device.objects.create(
            name='device1',
            description='my device',
            owner=user1,
        )


class DeviceModelTest(DeviceModelTestCase):

    def test_field_props(self):
        get_field = self.device1._meta.get_field

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
        user1 = self.device1.owner
        user1.delete()
        device_exists = Device.objects.filter(owner=user1).exists()

        self.assertFalse(device_exists)

    def test_device_to_str(self):
        device = self.device1
        device_as_str = f'{device.name} ({device.id})'

        self.assertEquals(str(device), device_as_str)

    def test_get_absolute_url(self):
        device = self.device1

        self.assertEquals(device.get_absolute_url(), '/devices/1/')


class DeviceImageModelTest(DeviceModelTestCase):

    def setUp(self):
        self.device_image1 = DeviceImage.objects.create(
            device=self.device1,
            description='device1-image',
        )

    def test_field_props(self):
        get_field = self.device_image1._meta.get_field

        device_field = get_field('device')
        self.assertEquals(device_field.db_constraint, True)
        self.assertEquals(device_field.many_to_one, True)
        self.assertEquals(device_field.null, False)
        self.assertEquals(device_field.remote_field.on_delete, models.CASCADE)

        image_field = get_field('image')
        self.assertEquals(image_field.default, 'default_device_pic.jpg')
        self.assertEquals(image_field.upload_to, 'device_pics')

        description_field = get_field('description')
        self.assertTrue(isinstance(description_field, models.TextField))

        create_date_field = get_field('create_date')
        self.assertEquals(create_date_field.auto_now_add, True)

        modified_date_field = get_field('modified_date')
        self.assertEquals(modified_date_field.auto_now, True)

    def test_try_create_device_image_without_device(self):
        with self.assertRaisesMessage(
                IntegrityError,
                'NOT NULL constraint failed: devices_deviceimage.device_id'):
            DeviceImage.objects.create()

    def test_cascade_delete_device_image(self):
        self.device1.delete()
        device_image_exists =\
            DeviceImage.objects.filter(device=self.device1).exists()

        self.assertFalse(device_image_exists)

    def test_device_image_to_str(self):
        device_image = self.device_image1

        self.assertEquals(str(device_image), 'Image (1) of device device1')

    def test_get_absolute_url(self):
        self.assertEquals(
            self.device_image1.get_absolute_url(), '/devices/1/images/1/')
