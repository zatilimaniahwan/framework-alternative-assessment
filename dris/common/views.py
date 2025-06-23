from django.shortcuts import render
from ShelterDirectory.models import Shelter
from DisasterReporting.models import DisasterReport
from AidRequestManagement.models import AidRequest
from VolunteerCoordination.models import Volunteer

# Create your views here.
def home_view(request):
    context = {
        'shelter_count': Shelter.objects.count(),
        'disaster_report_count': DisasterReport.objects.count(),
        'aid_request_count': AidRequest.objects.count(),
        'volunteer_count': Volunteer.objects.count(),
    }
    return render(request, 'components/home/index.html', context)