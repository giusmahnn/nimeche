from django.urls import path
from .views import (
    AdminDashboardView,
    LoginView,
    LogoutView,
)


urlpatterns = [
    path("custom-login/", LoginView.as_view(), name='admin-login'),
    path("dashboard/<str:username>/", AdminDashboardView.as_view(), name='admin-dashboard'),
    path("logout/", LogoutView.as_view(), name='admin-logout'),
]