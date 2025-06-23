from django.shortcuts import render, redirect
from django.views import View
from .models import Shelter
from UserManagement.models import Authority
from django.urls import reverse

def get_columns():
    return [
        {'key': 'code', 'label': 'Code'},
        {'key': 'name', 'label': 'Name'},
        {'key': 'location', 'label': 'Location'},
        {'key': 'capacity', 'label': 'Capacity'},
        {'key': 'availability', 'label': 'Availability'},
        {
            'label': 'Action',
            'type': 'action',
            'actions': [
                {
                    'url_name': '',
                    'label': 'Edit',
                    'class': 'btn-primary'
                }
            ]
        }
    ]

def get_field_config(edit_id=None, data=None):
    # data: dict of values to prefill, edit_id: disables code field if present
    data = data or {}
    return [
        {
            'type': 'text',
            'name': 'code',
            'label': 'Code',
            'placeholder': 'Code',
            'required': True,
            'disabled': bool(edit_id),
            'value': data.get('code', ''),
        },
        {
            'type': 'text',
            'name': 'name',
            'label': 'Name',
            'placeholder': 'Name',
            'required': True,
            'disabled': False,
            'value': data.get('name', ''),
        },
        {
            'type': 'text',
            'name': 'location',
            'label': 'Location',
            'placeholder': 'Location',
            'required': True,
            'disabled': False,
            'value': data.get('location', ''),
        },
        {
            'type': 'number',
            'name': 'capacity',
            'label': 'Capacity',
            'placeholder': 'Capacity',
            'required': True,
            'disabled': False,
            'value': data.get('capacity', ''),
        },
        {
            'type': 'select',
            'name': 'availability',
            'label': 'Availability',
            'options': [
                {'value': 1, 'label': 'Available'},
                {'value': 0, 'label': 'Not Available'}
            ],
            'required': True,
            'disabled': False,
            'value': data.get('availability', ''),
        }
    ]

class ShelterDirectoryView(View):
    def get(self, request):
        shelters = Shelter.objects.all()
        columns = get_columns()
        edit_id = request.GET.get('edit')
        show_modal = False
        fieldConfig = get_field_config()
        if edit_id:
            try:
                shelter = Shelter.objects.get(id=edit_id)
                shelter_data = {
                    'code': shelter.code,
                    'name': shelter.name,
                    'location': shelter.location,
                    'capacity': shelter.capacity,
                    'availability': int(shelter.availability),
                }
                fieldConfig = get_field_config(edit_id=edit_id, data=shelter_data)
                show_modal = True
            except Shelter.DoesNotExist:
                pass

        return render(request, 'shelter-directory/index.html', {
            'data': shelters,
            'columns': columns,
            'fieldConfig': fieldConfig,
            'show_modal': show_modal,
            'edit_id': edit_id or '',
        })

    def post(self, request):
        edit_id = request.POST.get('edit_id')
        # Gather posted data for prefill in case of errors
        data = {field['name']: request.POST.get(field['name'], '').strip() for field in get_field_config()}
        fieldConfig = get_field_config(edit_id=edit_id, data=data)

        errors = {}

        for field in fieldConfig:
            field_name = field['name']
            value = data.get(field_name, '')
            if field.get('required') and not value:
                errors[field_name] = f"{field['label']} is required."

        if data.get('capacity'):
            try:
                data['capacity'] = int(data['capacity'])
            except ValueError:
                errors['capacity'] = "Capacity must be a number."
        if data.get('availability'):
            try:
                data['availability'] = int(data['availability'])
            except ValueError:
                errors['availability'] = "Availability must be selected."

        if not edit_id and not errors and data.get('code'):
            if Shelter.objects.filter(code=data['code']).exists():
                errors['code'] = "Code already exists."

        if errors:
            shelters = Shelter.objects.all()
            columns = get_columns()
            return render(request, 'shelter-directory/index.html', {
                'data': shelters,
                'columns': columns,
                'fieldConfig': fieldConfig,
                'form_errors': errors,
                'show_modal': True,
                'edit_id': edit_id or '',
            })

        authority = None
        if request.user.is_authenticated:
            authority = Authority.objects.filter(user=request.user).first()

        if edit_id:
            try:
                shelter = Shelter.objects.get(id=edit_id)
                shelter.name = data['name']
                shelter.location = data['location']
                shelter.capacity = data['capacity']
                shelter.availability = bool(int(data['availability']))
                shelter.save()
            except Shelter.DoesNotExist:
                pass
        else:
            if authority:
                Shelter.objects.create(
                    code=data['code'],
                    name=data['name'],
                    location=data['location'],
                    capacity=data['capacity'],
                    availability=data['availability'],
                    created_by=authority,
                )
        return redirect(reverse('shelter:shelter_list'))

class ShelterDirectoryCardView(View):
    def get(self, request):
        # Get filter values from GET parameters
        name = request.GET.get('name', '').strip()
        code = request.GET.get('code', '').strip()
        location = request.GET.get('location', '').strip()
        availability = request.GET.get('availability', '').strip()

        shelters = Shelter.objects.all()
        if name:
            shelters = shelters.filter(name__icontains=name)
        if code:
            shelters = shelters.filter(code__icontains=code)
        if location:
            shelters = shelters.filter(location__icontains=location)
        if availability != '':
            shelters = shelters.filter(availability=availability)

        return render(request, 'shelter-directory/directory.html', {
            'data': shelters,
        })


