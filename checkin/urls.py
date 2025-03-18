from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.checkin_module, name="checkin_module"),  #  shows the check-in form
    path('checkin/', views.client_checkin, name="client_checkin"),  # handles check-in POST requests
    path('report/', views.checkin_report, name="checkin_report"),
]