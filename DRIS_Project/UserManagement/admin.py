from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Role, Volunteer, Authority, Citizen, Organization

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = list(BaseUserAdmin.fieldsets) + [
        ('Role Information', {'fields': ('role',)}),
    ]
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Volunteer)
admin.site.register(Authority)
admin.site.register(Citizen)
admin.site.register(Organization)