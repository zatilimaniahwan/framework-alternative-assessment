from django.db import models
from UserManagement.models import User
# Create your models here.

# Disaster Reporting Model
# This model is used to report disasters with details such as type, location, image, description, and status.
class DisasterReport(models.Model):
    id= models.AutoField(primary_key=True)
    reporter_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disaster_reports')
    type_of_disaster = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    image_upload = models.ImageField(upload_to='disaster_images/', blank=True, null=True)
    description = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Open', choices=[
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ])
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='disaster_reports_updated')
    
    def __str__(self):
        return f"{self.type_of_disaster} reported by {self.reporter_name.email} on {self.date_reported.strftime('%Y-%m-%d %H:%M:%S')}"