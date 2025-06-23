from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Role

def register_view(request):
    # Fetch all roles for the select options
    roles = Role.objects.all()
    role_options = [{'value': role.id, 'label': role.name} for role in roles]

    fieldConfig = [
        {'type': 'text', 'name': 'username', 'label': 'Username', 'placeholder': 'Username', 'required': True},
        {'type': 'email', 'name': 'email', 'label': 'Email', 'placeholder': 'Email', 'required': True},
        {'type': 'password', 'name': 'password', 'label': 'Password', 'placeholder': 'Password', 'required': True},
        {'type': 'password', 'name': 'confirm_password', 'label': 'Confirm Password', 'placeholder': 'Confirm Password', 'required': True},
        {'type': 'select', 'name': 'role', 'label': 'Role', 'options': role_options, 'required': True},
    ]
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role_id = request.POST.get('role', '')
        # Validation
        if not username: errors['username'] = 'Username is required.'
        if not email: errors['email'] = 'Email is required.'
        if not password: errors['password'] = 'Password is required.'
        if password != confirm_password: errors['confirm_password'] = 'Passwords do not match.'
        if not role_id: errors['role'] = 'Role is required.'
        if CustomUser.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists.'
        if CustomUser.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists.'
        if not errors:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            # Assign role if applicable
            try:
                role_obj = Role.objects.get(id=role_id)
                user.role = role_obj
                user.save()
            except Role.DoesNotExist:
                errors['role'] = 'Selected role does not exist.'
                return render(request, 'user/register.html', {'fieldConfig': fieldConfig, 'form_errors': errors})
            messages.success(request, "Registration successful. Please log in.")
            return redirect('auth:login')
    return render(request, 'user/register.html', {'fieldConfig': fieldConfig, 'form_errors': errors})

def login_view(request):
    fieldConfig = [
        {'type': 'text', 'name': 'username', 'label': 'Username', 'placeholder': 'Username', 'required': True},
        {'type': 'password', 'name': 'password', 'label': 'Password', 'placeholder': 'Password', 'required': True},
    ]
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            errors['__all__'] = 'Invalid username or password.'
    return render(request, 'user/login.html', {'fieldConfig': fieldConfig, 'form_errors': errors})

def logout_view(request):
    logout(request)
    return redirect('auth:login')
