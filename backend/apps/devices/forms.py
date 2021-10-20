from django import forms

from .models import DeviceImage


class DeviceImageEditForm(forms.ModelForm):

    class Meta:
        model = DeviceImage
        fields = ['device', 'image', 'description']
        widgets = {
            'device': forms.widgets.HiddenInput()
        }
