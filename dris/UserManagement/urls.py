from django.urls import path
from .views import  *
app_name = "auth"

urlpatterns = [
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register_view, name="register"),
    path('volunteers/', VolunteerDirectoryView.as_view(), name='volunteer_list'),
    path('citizens/', CitizenDirectoryView.as_view(), name='citizen_list'),
    path('authorities/', AuthorityDirectoryView.as_view(), name='authority_list'),
]