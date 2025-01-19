from django.urls import path
from .views import (
    LoginView,
    AdminDashboardView,
    ToggleVotingStatusView,
    LogoutView,
)


urlpatterns = [
    path("custom-login/", LoginView.as_view(), name='admin-login'),
    path("dashboard/<str:username>/", AdminDashboardView.as_view(), name='admin-dashboard'),
    path("toggle-voting-status/", ToggleVotingStatusView.as_view(), name='toggle-voting-status'),
    path("logout/", LogoutView.as_view(), name='admin-logout'),
]