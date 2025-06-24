# Author: Nurzatilimani binti Muhamad Ahwan
# Matric No: 24200114

from django.shortcuts import render
from ShelterDirectory.models import Shelter
from DisasterReporting.models import DisasterReport
from AidRequestManagement.models import AidRequest
from VolunteerCoordination.models import Volunteer, VolunteerTask
from UserManagement.models import Citizen

# Create your views here.
def home_view(request):
    user = request.user
    is_citizen = False
    is_authority = False
    is_volunteer = False
    show_disaster_and_aid = False
    show_all_cards = False
    show_shelter_and_volunteer = False

    disaster_report_count = 0
    aid_request_count = 0
    shelter_count = 0
    volunteer_count = 0
    assigned_task_count = 0

    if user.is_authenticated and hasattr(user, 'role') and user.role:
        role_name = user.role.name.lower()
        if role_name == 'citizens':
            is_citizen = True
            show_disaster_and_aid = True
            citizen = Citizen.objects.filter(user=user).first()
            if citizen:
                disaster_report_count = DisasterReport.objects.filter(reporter_name=citizen).count()
                aid_request_count = AidRequest.objects.filter(created_by=citizen).count()
        elif role_name == 'authorities':
            is_authority = True
            show_all_cards = True
            disaster_report_count = DisasterReport.objects.count()
            aid_request_count = AidRequest.objects.count()
            shelter_count = Shelter.objects.count()
            volunteer_count = Volunteer.objects.count()
        elif role_name == 'volunteers':
            is_volunteer = True
            volunteer = Volunteer.objects.filter(user=user).first()
            show_shelter_and_volunteer = True
            shelter_count = Shelter.objects.count()
            volunteer_count = Volunteer.objects.count()
            if volunteer:
                assigned_task_count = VolunteerTask.objects.filter(volunteers=volunteer).count()
    elif not user.is_authenticated:
        show_shelter_and_volunteer = True
        shelter_count = Shelter.objects.count()
        volunteer_count = Volunteer.objects.count()

    context = {
        'is_citizen': is_citizen,
        'is_authority': is_authority,
        'is_volunteer': is_volunteer,
        'show_disaster_and_aid': show_disaster_and_aid,
        'show_all_cards': show_all_cards,
        'show_shelter_and_volunteer': show_shelter_and_volunteer,
        'disaster_report_count': disaster_report_count,
        'aid_request_count': aid_request_count,
        'shelter_count': shelter_count,
        'volunteer_count': volunteer_count,
        'assigned_task_count': assigned_task_count,
    }
    return render(request, 'components/home/index.html', context)