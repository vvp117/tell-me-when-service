from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


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
