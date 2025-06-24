from django.db import models
from UserManagement.models import Citizen, Authority
from ShelterDirectory.models import  Shelter
# Create your models here.

# This model represents an aid request made by a user for assistance, which can be related to a specific shelter or general aid.
class AidRequest(models.Model):
    id = models.AutoField(primary_key=True)
    requester_name = models.CharField(max_length=255)
    aid_type = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    shelter_id = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='aid_requests', null=True, blank=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=255)
    status = models.CharField(max_length=50, choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed')
    ], default='open')
    created_by = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='created_aid_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Authority, on_delete=models.CASCADE, related_name='updated_aid_requests', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Aid Request {self.id} by {self.requester_name} for {self.aid_type} at {self.address}"