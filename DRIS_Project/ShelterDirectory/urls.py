# Author: Nurzatilimani binti Muhamad Ahwan
# Matric No: 24200114

from django.urls import path
from .views import  *
app_name = "shelter"

urlpatterns = [
    path("list", ShelterDirectoryView.as_view(), name="shelter_list"),
    path("directory", ShelterDirectoryCardView.as_view(), name="shelter_directory"),
]