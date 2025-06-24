from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Role, Organization, Authority, Volunteer, Citizen

def register_view(request):
    roles = Role.objects.all()
    role_options = [{'value': role.name, 'label': role.name.capitalize()} for role in roles]
    organizations = Organization.objects.all()
    organization_options = [{'value': org.name, 'label': org.name} for org in organizations]

    fieldConfig = [
        {'type': 'text', 'name': 'username', 'label': 'Username', 'required': True},
        {'type': 'email', 'name': 'email', 'label': 'Email', 'required': True},
        {'type': 'password', 'name': 'password', 'label': 'Password', 'required': True},
        {'type': 'password', 'name': 'confirm_password', 'label': 'Confirm Password', 'required': True},
        {'type': 'select', 'name': 'role', 'label': 'Role', 'options': role_options, 'required': True},
        {'type': 'select', 'name': 'organization', 'label': 'Organization', 'options': organization_options, 'required': True, 'show_for': ['authorities']},
        {'type': 'text', 'name': 'address', 'label': 'Address', 'required': True, 'show_for': ['citizens']},
        {'type': 'text', 'name': 'state', 'label': 'State', 'required': True, 'show_for': ['citizens']},
        {'type': 'text', 'name': 'skills', 'label': 'Skills', 'required': True, 'show_for': ['volunteers']},
        {'type': 'checkbox', 'name': 'availability_status', 'label': 'Available?', 'required': True, 'show_for': ['volunteers']},
        {'type': 'datetime-local', 'name': 'availability_date_time', 'label': 'Available Date/Time', 'required': True, 'show_for': ['volunteers']},
        {'type': 'text', 'name': 'availability_location', 'label': 'Available Location', 'required': True, 'show_for': ['volunteers']},
    ]

    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role_name = request.POST.get('role', '')
        role_obj = Role.objects.filter(name=role_name).first()

        # Validation
        if not username: errors['username'] = 'Username is required.'
        if not email: errors['email'] = 'Email is required.'
        if not password: errors['password'] = 'Password is required.'
        if password != confirm_password: errors['confirm_password'] = 'Passwords do not match.'
        if not role_name: errors['role'] = 'Role is required.'
        if CustomUser.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists.'
        if CustomUser.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists.'

        # Dynamic validation
        if role_name == 'authorities' and not request.POST.get('organization'):
            errors['organization'] = 'Organization is required.'
        if role_name == 'citizens':
            if not request.POST.get('address'):
                errors['address'] = 'Address is required.'
            if not request.POST.get('state'):
                errors['state'] = 'State is required.'
        if role_name == 'volunteers':
            if not request.POST.get('skills'):
                errors['skills'] = 'Skills are required.'

        if not errors:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.role = role_obj
            user.save()

            if role_name == 'authorities':
                org_id = request.POST.get('organization')
                org = Organization.objects.get(name=org_id) if org_id else None
                Authority.objects.create(user=user, organization_id=org)
            elif role_name == 'citizens':
                Citizen.objects.create(
                    user=user,
                    address=request.POST.get('address', ''),
                    state=request.POST.get('state', '')
                )
            elif role_name == 'volunteers':
                Volunteer.objects.create(
                    user=user,
                    skills=request.POST.get('skills', ''),
                    availability_status=bool(request.POST.get('availability_status')),
                    availability_date_time=request.POST.get('availability_date_time') or None,
                    availability_location=request.POST.get('availability_location', '')
                )
            messages.success(request, "Registration successful. Please log in.")
            return redirect('auth:login')

    return render(request, 'user/register.html', {
        'fieldConfig': fieldConfig,
        'form_errors': errors,
    })

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
