from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import DeviceImage


@receiver(post_delete, sender=DeviceImage)
def delete_device_image_files(sender, instance: DeviceImage, **kwargs):
    path = instance.image.path
    default_image = instance.is_default_image(DeviceImage.image.field)
    if path and not default_image:
        default_storage.delete(path)
