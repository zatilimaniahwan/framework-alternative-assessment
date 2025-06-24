from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import VolunteerTask
from ShelterDirectory.models import Shelter
from UserManagement.models import Authority, Volunteer
from django.urls import reverse
import re
from django.contrib import messages
from django.http import HttpResponseRedirect

def get_volunteer_task_columns():
    return [
        {'key': 'task_name', 'label': 'Task Name'},
        {'key': 'shelter', 'label': 'Shelter'},
        {'key': 'skills', 'label': 'Skills'},
        {'key': 'status', 'label': 'Status'},
        {'key': 'created_date', 'label': 'Created Date'},
        {
            'label': 'Action',
            'type': 'action',
            'actions': [
                {
                    'label': 'Edit',
                    'class': 'btn-info'
                },
                {
                    'url_name': 'volunteer:volunteer_list_by_task',  
                    'label': 'View Volunteers',
                    'class': 'btn-success'
                }
            ]
        }
    ]

def get_volunteer_task_field_config(edit_id=None, data=None, is_edit=False):
    data = data or {}
    volunteers_qs = Volunteer.objects.all()
    shelters_qs = Shelter.objects.all()
    fields = [
        {
            'type': 'text',
            'name': 'task_name',
            'label': 'Task Name',
            'placeholder': 'Task Name',
            'required': True,
            'disabled': False,
            'value': data.get('task_name', ''),
        },
        {
            'type': 'select',
            'name': 'shelter',
            'label': 'Shelter',
            'options': [
                {'value': s.id, 'label': s.name} for s in shelters_qs
            ],
            'required': True,
            'disabled': False,
            'value': data.get('shelter', ''),
        },
        {
            'type': 'textarea',
            'name': 'skills',
            'label': 'Skills',
            'placeholder': 'Skills',
            'required': False,
            'disabled': False,
            'value': data.get('skills', ''),
        },
    ]
    if is_edit:
        fields.append({
            'type': 'select',
            'name': 'status',
            'label': 'Status',
            'options': [
                {'value': 'running', 'label': 'Running'},
                {'value': 'completed', 'label': 'Completed'},
                {'value': 'cancelled', 'label': 'Cancelled'},
            ],
            'required': True,
            'disabled': False,
            'value': data.get('status', 'running'),
        })
    return fields

class VolunteerTaskView(View):
    def get(self, request):
        tasks = VolunteerTask.objects.all()
        columns = get_volunteer_task_columns()
        edit_id = request.GET.get('edit')
        show_modal = False
        is_edit = bool(edit_id)
        fieldConfig = get_volunteer_task_field_config(edit_id=edit_id, is_edit=is_edit)
        user_role = ''
        if request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role:
            user_role = request.user.role.name.lower()
        if edit_id:
            try:
                task = VolunteerTask.objects.get(id=edit_id)
                task_data = {
                    'task_name': task.task_name,
                    'shelter': task.shelter.id if task.shelter else '',
                    'skills': task.skills,
                    'status': task.status,
                }
                fieldConfig = get_volunteer_task_field_config(edit_id=edit_id, data=task_data, is_edit=True)
                show_modal = True
            except VolunteerTask.DoesNotExist:
                pass

        return render(request, 'volunteer-coordination/volunteer-task/index.html', {
            'data': tasks,
            'columns': columns,
            'fieldConfig': fieldConfig,
            'show_modal': show_modal,
            'edit_id': edit_id or '',
            'user_role': user_role,
        })

    def post(self, request):
        edit_id = request.POST.get('edit_id')
        is_edit = bool(edit_id)
        data = {field['name']: request.POST.getlist(field['name']) if field['type'] == 'multiselect' else request.POST.get(field['name'], '').strip() for field in get_volunteer_task_field_config(is_edit=is_edit)}
        fieldConfig = get_volunteer_task_field_config(edit_id=edit_id, data=data, is_edit=is_edit)

        errors = {}

        for field in fieldConfig:
            field_name = field['name']
            value = data.get(field_name, '')
            if field.get('required') and (not value or (isinstance(value, list) and not any(value))):
                errors[field_name] = f"{field['label']} is required."

        if errors:
            tasks = VolunteerTask.objects.all()
            columns = get_volunteer_task_columns()
            return render(request, 'volunteer-coordination/volunteer-task/index.html', {
                'data': tasks,
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
                task = VolunteerTask.objects.get(id=edit_id)
                task.task_name = data['task_name']
                task.shelter = Shelter.objects.get(id=data['shelter'])
                task.skills = data['skills']
                task.status = data['status']
                task.save()
            except VolunteerTask.DoesNotExist:
                pass
        else:
            if authority:
                task = VolunteerTask.objects.create(
                    task_name=data['task_name'],
                    shelter_id=data['shelter'],
                    skills=data['skills'],
                    status='running',  # Default status on create
                    created_by=authority,
                )
        return redirect(reverse('volunteer:task_list'))

class VolunteerListByTaskSkillView(View):
    def get(self, request, task_id):
        task = get_object_or_404(VolunteerTask, id=task_id)
        # Handle None, empty, or whitespace-only task skills
        task_skills_val = (task.skills or '').strip()
        task_words = set(re.findall(r'\w+', task_skills_val.lower())) if task_skills_val else set()
        # Exclude volunteers with None, empty, or whitespace-only skills
        volunteers = Volunteer.objects.filter(
            availability_status=True
        ).exclude(skills__isnull=True).exclude(skills__exact='').exclude(skills__regex=r'^\s*$')

        filtered_volunteers = []
        for volunteer in volunteers:
            skills_val = (volunteer.skills or '').strip()
            if not skills_val:
                continue
            volunteer_words = set(re.findall(r'\w+', skills_val.lower()))
            if task_words:
                # Only add if there's a match
                if volunteer_words and (task_words & volunteer_words):
                    filtered_volunteers.append(volunteer)
            else:
                # If no task skills, only add if volunteer has non-empty, non-whitespace skills
                filtered_volunteers.append(volunteer)

        columns = [
            {'key': 'user__first_name', 'label': 'First Name'},
            {'key': 'user__last_name', 'label': 'Last Name'},
            {'key': 'user__email', 'label': 'Email'},
            {'key': 'skills', 'label': 'Skills'},
            {'key': 'availability_status', 'label': 'Available'},
            {
                'label': 'Action',
                'type': 'action',
                'actions': [
                    {
                        'label': 'Assign to Task',
                        'class': 'btn-warning'
                    }
                ]
            }
        ]

        data = []
        assigned_volunteers = set(task.volunteers.values_list('user_id', flat=True))
        for v in filtered_volunteers:
            data.append({
                'id': v.user.id,
                'user__first_name': v.user.first_name or v.user.username or v.user.email,
                'user__last_name': v.user.last_name or '',
                'user__email': v.user.email,
                'skills': v.skills,
                'availability_status': "Yes" if v.availability_status else "No",
                'assigned': v.user.id in assigned_volunteers,
            })

        user_role = ''
        if request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role:
            user_role = request.user.role.name.lower()

        return render(request, 'volunteer-coordination/volunteer-task/index.html', {
            'task': task,
            'columns': columns,
            'data': data,
            'show_volunteer_list': True,
            'user_role': user_role,
        })

class AssignVolunteerToTaskView(View):
    def post(self, request, task_id, volunteer_id):
        task = get_object_or_404(VolunteerTask, id=task_id)
        if task.status != "running":
            messages.error(request, f"Cannot assign volunteers to a task that is not running.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        volunteer = get_object_or_404(Volunteer, user_id=volunteer_id)
        task.volunteers.add(volunteer)
        task.save()
        messages.success(request, f"{volunteer.user.get_full_name() or volunteer.user.username} assigned to '{task.task_name}'.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
