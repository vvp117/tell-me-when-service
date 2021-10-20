from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

from PIL import Image


class Device(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('devices-item', kwargs={"pk": self.pk})


class DeviceImage(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    image = models.ImageField(default='default_device_pic.jpg',
                              upload_to='device_pics')
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Image ({self.pk}) of device {self.device.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        max_height = 768
        max_width = 1024
        if img.height > max_height or img.width > max_width:
            img.thumbnail((max_height, max_width))
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('devices-images-edit',
                       kwargs={'device_pk': self.device.pk, 'pk': self.pk})

    def is_default_image(self, field: models.FileField):
        default_url = f'{default_storage.base_url}{field.default}'
        return getattr(self, field.name).url == default_url
