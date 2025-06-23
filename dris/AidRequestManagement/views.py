from django.shortcuts import render, redirect
from django.views import View
from .models import AidRequest
from UserManagement.models import Citizen, Authority
from ShelterDirectory.models import Shelter
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def get_aid_request_columns():
    return [
        {'key': 'id', 'label': 'ID'},
        {'key': 'requester_name', 'label': 'Requester'},
        {'key': 'aid_type', 'label': 'Aid Type'},
        {'key': 'status', 'label': 'Status'},
        {
            'label': 'Action',
            'type': 'action',
            'actions': [
                {
                    'url_name': '',
                    'label': 'Edit',
                    'class': 'btn-info'
                }
            ]
        }
    ]

def get_aid_request_field_config(edit_id=None, data=None, request=None, is_edit=False):
    data = data or {}
    # Set requester_name value and disabled if request is provided and user is authenticated
    requester_value = data.get('requester_name', '')
    requester_disabled = False
    if request and request.user.is_authenticated:
        full_name = f"{request.user.first_name} {request.user.last_name}".strip()
        requester_value = full_name if full_name else (request.user.username or request.user.email)
        requester_disabled = True

    # Status field: only show for authorities when editing
    show_status = True
    status_field = {
        'type': 'select',
        'name': 'status',
        'label': 'Status',
        'options': [
            {'value': 'open', 'label': 'Open'},
            {'value': 'in_progress', 'label': 'In Progress'},
            {'value': 'completed', 'label': 'Completed'},
            {'value': 'closed', 'label': 'Closed'},
        ],
        'required': True,
        'value': data.get('status', 'open'),
    }
    if is_edit:
        # Only show status if user is authority
        show_status = request and hasattr(request.user, 'role') and request.user.role and request.user.role.name.lower() == "authorities"
    elif not (request and hasattr(request.user, 'role') and request.user.role and request.user.role.name.lower() == "authorities"):
        show_status = False

    # Aid type as select
    aid_type_value = data.get('aid_type', '')
    aid_type_field = {
        'type': 'select',
        'name': 'aid_type',
        'label': 'Aid Type',
        'required': True,
        'options': [
            {'value': 'food', 'label': 'Food'},
            {'value': 'shelter', 'label': 'Shelter'},
            {'value': 'rescue', 'label': 'Rescue'},
        ],
        'value': aid_type_value,
    }

    # Shelter field: only show if aid_type is 'shelter'
    shelter_field = None
    
    available_shelters = Shelter.objects.filter(availability=True)
    shelter_field = {
        'type': 'select',
        'name': 'shelter_id',
        'label': 'Shelter',
        'required': aid_type_value.lower() == 'shelter',
        'options': [
            {'value': shelter.id, 'label': f"{shelter.code} - {shelter.name} ({shelter.location})"}
            for shelter in available_shelters
        ],
        'value': data.get('shelter_id', ''),
    }

    fields = [
        {
            'type': 'text',
            'name': 'requester_name',
            'label': 'Requester',
            'required': False,
            'value': requester_value,
            'disabled': requester_disabled,
        },
        aid_type_field,
        {'type': 'textarea', 'name': 'description', 'label': 'Description', 'required': True, 'value': data.get('description', '')},
        shelter_field,
        {'type': 'text', 'name': 'address', 'label': 'Address', 'required': True, 'value': data.get('address', '')},
        {'type': 'text', 'name': 'phone_number', 'label': 'Phone', 'required': True, 'value': data.get('phone_number', '')},
        {'type': 'text', 'name': 'email', 'label': 'Email', 'required': True, 'value': data.get('email', '')},
    ]
    if show_status:
        fields.append(status_field)
    return fields

class AidRequestView(View):
    def get(self, request):
        aid_requests = AidRequest.objects.all()
        columns = get_aid_request_columns()
        edit_id = request.GET.get('edit')
        show_modal = False
        data = request.GET if request.GET else None
        fieldConfig = get_aid_request_field_config(data=data, request=request)
        if edit_id:
            try:
                aid = AidRequest.objects.get(id=edit_id)
                aid_data = {
                    'requester_name': aid.requester_name,
                    'aid_type': aid.aid_type,
                    'description': aid.description,
                    'shelter_id': aid.shelter_id.id if aid.shelter_id else '',
                    'address': aid.address,
                    'phone_number': aid.phone_number,
                    'email': aid.email,
                    'status': aid.status,
                }
                fieldConfig = get_aid_request_field_config(edit_id=edit_id, data=aid_data, request=request, is_edit=True)
                show_modal = True
            except AidRequest.DoesNotExist:
                pass
        # Show modal if aid_type is present in GET (user changed aid_type)
        elif request.GET.get('aid_type'):
            show_modal = True

        return render(request, 'aid-request/index.html', {
            'data': aid_requests,
            'columns': columns,
            'fieldConfig': fieldConfig,
            'show_modal': show_modal,
            'edit_id': edit_id or '',
        })

    def post(self, request):
        edit_id = request.POST.get('edit_id')
        is_edit = bool(edit_id)
        # Build data from POST first
        data = {key: request.POST.get(key, '').strip() for key in request.POST.keys()}
        # Now build fieldConfig with this data
        fieldConfig = get_aid_request_field_config(edit_id=edit_id, data=data, request=request, is_edit=is_edit)
        errors = {}

        for field in fieldConfig:
            if field.get('required') and not data.get(field['name']):
                errors[field['name']] = f"{field['label']} is required."

        if errors:
            logger.error(f"AidRequest POST validation errors: {errors} | Data: {data}")
            aid_requests = AidRequest.objects.all()
            columns = get_aid_request_columns()
            return render(request, 'aid-request/index.html', {
                'data': aid_requests,
                'columns': columns,
                'fieldConfig': fieldConfig,
                'form_errors': errors,
                'show_modal': True,
                'edit_id': edit_id or '',
            })

        citizen = None
        if request.user.is_authenticated:
            citizen = Citizen.objects.filter(user=request.user).first()
        if citizen:
            full_name = f"{citizen.user.first_name} {citizen.user.last_name}".strip()
            requester_name = full_name if full_name else (citizen.user.username or citizen.user.email)
            try:
                AidRequest.objects.create(
                    aid_type=data['aid_type'],
                    description=data['description'],
                    address=data['address'],
                    phone_number=data['phone_number'],
                    status=data.get('status', 'open'),
                    requester_name=requester_name,
                    created_by=citizen,
                    shelter_id=data.get('shelter_id') or None,
                    email=data.get('email', ''),
                )
            except Exception as e:
                logger.error(f"Error creating AidRequest: {e} | Data: {data}")
        else:
            logger.error(f"No citizen found for user {request.user} | Data: {data}")
        return redirect(request.path)
