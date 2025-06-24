# Author: Nurzatilimani binti Muhamad Ahwan
# Matric No: 24200114

from django.urls import path
from .views import  *
app_name = "aid"

urlpatterns = [
    path("list", AidRequestView.as_view(), name="aid_request_list"),
]

