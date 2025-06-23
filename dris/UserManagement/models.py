from django.db import models

# Create your models here.
# This file defines the User and Role models for the User Management module.
# The User model represents a user in the system, while the Role model defines the different roles a user can have.

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

# This model represents a user in the system.
# It includes fields for the user's name, phone number, email, password, role, and the date the user was created.
# The email field is unique and is used for login purposes.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True) # used for login
    password = models.CharField(max_length=128)  # Store hashed passwords
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email