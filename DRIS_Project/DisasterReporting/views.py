# Author: Nurzatilimani binti Muhamad Ahwan
# Matric No: 24200114

from django.shortcuts import render, redirect
from django.views import View
from .models import DisasterReport
from UserManagement.models import Citizen
import logging

logger = logging.getLogger(__name__)

def get_disaster_report_columns():
    return [
        {'key': 'disaster_type', 'label': 'Type'},
        {'key': 'gps_coordinates', 'label': 'Location'},
        {'key': 'severity_level', 'label': 'Severity'},
        {'key': 'description', 'label': 'Description'},
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

def get_disaster_report_field_config(edit_id=None, data=None, request=None, is_edit=False):
    data = data or {}
    # Set reporter_name value and disabled if request is provided and user is authenticated
    reporter_value = data.get('reporter_name', '')
    reporter_disabled = False
    status_value = data.get('status', 'Open')
    status_disabled = False

    if request and request.user.is_authenticated:
        citizen = Citizen.objects.filter(user=request.user).first()
        if citizen:
            full_name = f"{citizen.user.first_name} {citizen.user.last_name}".strip()
            reporter_value = full_name if full_name else (citizen.user.username or citizen.user.email)
            reporter_disabled = True

    # Status field: only show for authorities when editing
    show_status = True
    if is_edit:
        show_status = request and hasattr(request.user, 'role') and request.user.role and request.user.role.name.lower() == "authorities"
    elif not (request and hasattr(request.user, 'role') and request.user.role and request.user.role.name.lower() == "authorities"):
        show_status = False

    status_field = {
        'type': 'select',
        'name': 'status',
        'label': 'Status',
        'options': [
            {'value': 'Open', 'label': 'Open'},
            {'value': 'In Progress', 'label': 'In Progress'},
            {'value': 'Resolved', 'label': 'Resolved'},
            {'value': 'Closed', 'label': 'Closed'},
        ],
        'required': True,
        'value': status_value,
        'disabled': status_disabled,
    }

    fields = [
        {
            'type': 'text',
            'name': 'reporter_name',
            'label': 'Reporter',
            'required': False,
            'value': reporter_value,
            'disabled': reporter_disabled,
        },
        {
            'type': 'text',
            'name': 'disaster_type',
            'label': 'Disaster Type',
            'required': True,
            'value': data.get('disaster_type', ''),
        },
        {
            'type': 'text',
            'name': 'gps_coordinates',
            'label': 'GPS Coordinates',
            'required': True,
            'value': data.get('gps_coordinates', ''),
        },
        {
            'type': 'select',
            'name': 'severity_level',
            'label': 'Severity Level',
            'required': True,
            'options': [
                {'value': 'Low', 'label': 'Low'},
                {'value': 'Medium', 'label': 'Medium'},
                {'value': 'High', 'label': 'High'},
                {'value': 'Critical', 'label': 'Critical'},
            ],
            'value': data.get('severity_level', 'Low'),
        },
        {
            'type': 'textarea',
            'name': 'description',
            'label': 'Description',
            'required': False,
            'value': data.get('description', ''),
        },
    ]
    if show_status:
        fields.append(status_field)
    return fields

class DisasterReportView(View):
    def get(self, request):
        search_query = request.GET.get('search', '').strip()
        reports = DisasterReport.objects.all()
        if search_query:
            reports = reports.filter(
                disaster_type__icontains=search_query
            ) | reports.filter(
                description__icontains=search_query
            ) | reports.filter(
                gps_coordinates__icontains=search_query
            ) | reports.filter(
                severity_level__icontains=search_query
            ) | reports.filter(
                status__icontains=search_query
            )
        columns = get_disaster_report_columns()
        edit_id = request.GET.get('edit')
        show_modal = False
        data = request.GET if request.GET else None
        fieldConfig = get_disaster_report_field_config(data=data, request=request)
        user_role = ''
        if request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role:
            user_role = request.user.role.name.lower()
        if edit_id:
            try:
                report = DisasterReport.objects.get(id=edit_id)
                report_data = {
                    'reporter_name': f"{report.reporter_name.user.first_name} {report.reporter_name.user.last_name}".strip() or report.reporter_name.user.username or report.reporter_name.user.email,
                    'disaster_type': report.disaster_type,
                    'gps_coordinates': report.gps_coordinates,
                    'severity_level': report.severity_level,
                    'description': report.description,
                    'status': report.status,
                }
                fieldConfig = get_disaster_report_field_config(edit_id=edit_id, data=report_data, request=request, is_edit=True)
                show_modal = True
            except DisasterReport.DoesNotExist:
                pass
        elif request.GET.get('disaster_type'):
            show_modal = True

        return render(request, 'disaster-report/index.html', {
            'data': reports.distinct(),
            'columns': columns,
            'fieldConfig': fieldConfig,
            'show_modal': show_modal,
            'edit_id': edit_id or '',
            'user_role': user_role,
            'search_query': search_query,
        })

    def post(self, request):
        edit_id = request.POST.get('edit_id')
        is_edit = bool(edit_id)
        data = {key: request.POST.get(key, '').strip() for key in request.POST.keys()}
        fieldConfig = get_disaster_report_field_config(edit_id=edit_id, data=data, request=request, is_edit=is_edit)
        errors = {}

        for field in fieldConfig:
            if field.get('required') and not data.get(field['name']):
                errors[field['name']] = f"{field['label']} is required."

        if errors:
            logger.error(f"DisasterReport POST validation errors: {errors} | Data: {data}")
            reports = DisasterReport.objects.all()
            columns = get_disaster_report_columns()
            return render(request, 'disaster-report/index.html', {
                'data': reports,
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
            try:
                DisasterReport.objects.create(
                    reporter_name=citizen,
                    disaster_type=data['disaster_type'],
                    gps_coordinates=data['gps_coordinates'],
                    severity_level=data['severity_level'],
                    description=data['description'],
                    status=data.get('status', 'Open'),
                    updated_by=request.user,
                )
            except Exception as e:
                logger.error(f"Error creating DisasterReport: {e} | Data: {data}")
        else:
            logger.error(f"No citizen found for user {request.user} | Data: {data}")
        return redirect(request.path)
