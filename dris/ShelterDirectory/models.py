from django.db import models
from UserManagement.models import User
# Create your models here.

# District model to store information about districts
# Each district has a unique postcode and a name
# The __str__ method returns the postcode for easy identification
class District(models.Model):
    id = models.AutoField(primary_key=True)
    postcode = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.postcode

# State model to store information about states
# Each state has a unique code, name, and a foreign key to the District model
# The foreign key establishes a many-to-one relationship with District, meaning each state belongs to one district
# The __str__ method returns the state code for easy identification
class State(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='states')

    def __str__(self):
        return self.code

# Shelter model to store information about shelters
# Each shelter has a unique code, name, address, state, postcode, district, phone, capacity, availability, and timestamps for creation and updates
# It also has foreign keys to the User model for tracking who created and updated the shelter
class Shelter(models.Model):
    id= models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    postcode=models.CharField(max_length=5)
    district = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    capacity = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shelters_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shelters_updated', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code