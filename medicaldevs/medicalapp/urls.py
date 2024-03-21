from django.urls import path
from . import views

urlpatterns = [
    path('add_description/', views.add_description, name = 'add_description'),
]