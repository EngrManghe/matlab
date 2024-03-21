from django.db import models

class MedicalDevice(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        app_label = 'medicalapp'  # Specify the app_label for the model