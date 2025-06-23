from django.db import models
from UserManagement.models import Volunteer, Authority
from ShelterDirectory.models import Shelter

# Create your models here.
# VolunteerAssignments model to manage volunteer assignments to shelters
class VolunteerAssignments(models.Model):
    id = models.AutoField(primary_key=True)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='assignments')
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='volunteer_assignments')
    assigned_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('assigned', 'Assigned'), ('completed', 'Completed')], default='assigned')
    created_by = models.ForeignKey(Authority, on_delete=models.CASCADE, related_name='created_assignments', null=True, blank=True)
    
    def __str__(self):
        return f"{self.volunteer.user} - {self.shelter.name} ({self.status})"
