# Author: Nurzatilimani binti Muhamad Ahwan
# Matric No: 24200114

from django.db import models
from UserManagement.models import Citizen, CustomUser
# Create your models here.

# Disaster Reporting Model
# This model is used to report disasters with details such as type, location, image, description, and status.
class DisasterReport(models.Model):
    id= models.AutoField(primary_key=True)
    reporter_name = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='disaster_reports')
    disaster_type = models.CharField(max_length=100)
    gps_coordinates = models.CharField(max_length=100, help_text='Enter GPS coordinates in the format: latitude,longitude')
    severity_level = models.CharField(max_length=50, choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ], default='Low', help_text='Select the severity level of the disaster')
    description = models.TextField(blank=True, null=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Open', choices=[
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ])
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='disaster_reports_updated')
    
    def __str__(self):
        return f"{self.disaster_type} reported by {self.reporter_name.user.username} on {self.date_reported.strftime('%Y-%m-%d %H:%M:%S')}"