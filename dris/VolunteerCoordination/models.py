from django.db import models
from UserManagement.models import Volunteer, Authority
from ShelterDirectory.models import Shelter

# Create your models here.
# VolunteerAssignments model to manage volunteer assignments to shelters
class VolunteerAssignments(models.Model):
    id = models.AutoField(primary_key=True)
    volunteer = models.CharField(max_length=255, blank=False)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='volunteer_assignments')
    assigned_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('assigned', 'Assigned'), ('completed', 'Completed')], default='assigned')
    created_by = models.ForeignKey(Authority, on_delete=models.CASCADE, related_name='created_assignments', null=True, blank=True)
    
    def __str__(self):
        return f"{self.volunteer} - {self.shelter.name} ({self.status})"

class VolunteerTask(models.Model):
    id = models.AutoField(primary_key=True)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='tasks')
    task_name = models.CharField(max_length=255)
    skills = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('running', 'Running'), ('completed', 'Completed'), ('cancelled', 'Cancelled')],
        default='running'
    )
    created_by = models.ForeignKey(Authority, on_delete=models.CASCADE, related_name='created_tasks', null=True, blank=True)
    volunteers = models.ManyToManyField('UserManagement.Volunteer', related_name='assigned_tasks', blank=True)

    def __str__(self):
        return f"{self.task_name} at {self.shelter.name} ({self.status})"
