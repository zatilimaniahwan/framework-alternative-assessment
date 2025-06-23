from django.db import models
from UserManagement.models import Authority
# Create your models here.
# Shelter model to store information about shelters
class Shelter(models.Model):
    id= models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)
    created_by = models.ForeignKey(Authority, on_delete=models.CASCADE, related_name='shelters_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Authority, on_delete=models.CASCADE, related_name='shelters_updated', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code
    