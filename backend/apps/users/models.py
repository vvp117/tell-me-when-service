from django.db import models
from django.contrib.auth.models import User

from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile_pic.jpg',
                              upload_to='profile_pics')

    def __str__(self) -> str:
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        max_height = 300
        max_width = 300
        if img.height > max_height or img.width > max_width:
            img.thumbnail((max_height, max_width))
            img.save(self.image.path)
