from django.shortcuts import render
from django.views import View
from .models import Shelter

# Create your views here.
class ShelterDirectoryView(View):
    def get(self, request):
        shelters = Shelter.objects.all()
        columns = [
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
                        'label': 'View',
                        'class': 'btn-primary'
                    }
                ]
            }
        ]
        return render(request, 'shelter-directory/index.html', {
            'data': shelters,
            'columns': columns
        })