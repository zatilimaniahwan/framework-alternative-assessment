# Author: Nurzatilimani binti Muhamad Ahwan
# Matric No: 24200114

from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = [
            '/shelter/list',
            '/disaster-reporting/list',
            '/auth/volunteers/',
            '/auth/citizens/',
            '/auth/authorities/',
            '/aid/list',
            '/volunteer/volunteer-tasks/list',
        ]
        auth_paths = [
            reverse('auth:login'),
            reverse('auth:register'),
        ]
        # Redirect authenticated users away from login/register
        if request.user.is_authenticated and request.path in auth_paths:
            return redirect('home') 

        # Redirect unauthenticated users from restricted paths
        if any(request.path.startswith(path) for path in restricted_paths):
            if not request.user.is_authenticated:
                return redirect(reverse('auth:login'))
        return self.get_response(request)