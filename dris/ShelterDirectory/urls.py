from django.urls import path
from .views import  *
app_name = "shelter"

urlpatterns = [
    path("list", ShelterDirectoryView.as_view(), name="shelter_list"),
]