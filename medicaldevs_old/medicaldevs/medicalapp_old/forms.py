from django import forms
from .models import MedicalDevice

class MedicalDeviceForm(forms.ModelForm):
    class Meta:
        model = MedicalDevice
        fields = ['name', 'description']