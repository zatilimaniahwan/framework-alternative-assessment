from django.db import models
from django.contrib.auth.models import AbstractUser

# Role model defines the different roles a user can have.
class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        unique=True,
        choices=[
            ('authorities', 'Authorities'),
            ('citizens', 'Citizens'),
            ('volunteers', 'Volunteers'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Custom user model extending Django's AbstractUser and adding a role field.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# This model represents a volunteer in the system.
class Volunteer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    skills = models.TextField(blank=True, null=True)
    availability_status = models.BooleanField(default=True)
    availability_date_time = models.DateTimeField(blank=True, null=True)
    availability_location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Volunteer: {self.user.email}"

# This model represents a citizen in the system.
class Citizen(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='citizens')
    address = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Citizen: {self.user.email}"

# Organization model represents an organization in the system.
class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_organizations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='updated_organizations', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# This model represents an authority in the system.
class Authority(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='authorities')
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='authorities', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)