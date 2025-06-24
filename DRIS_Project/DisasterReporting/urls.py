# Author: Nurzatilimani binti Muhamad Ahwan
# Matric No: 24200114

from django.urls import path
from .views import  *
app_name = "disaster-reporting"

urlpatterns = [
    path("list", DisasterReportView.as_view(), name="disaster_report_list"),
]