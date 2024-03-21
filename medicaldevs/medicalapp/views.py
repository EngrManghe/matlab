from django.shortcuts import render
from .forms import MedicalDeviceForm

def add_description(request):
    if request.method == 'POST':
        form = MedicalDeviceForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        print("you")
        form = MedicalDeviceForm()

    return render(request, 'medicalapp/add_description.html', {'form': form})
