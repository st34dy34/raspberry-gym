from django.urls import path
from .views import CheckinModuleView, ClientCheckinView, CheckinReportView

urlpatterns = [
    path('', CheckinModuleView.as_view(), name="checkin_module"),
    path('checkin/', ClientCheckinView.as_view(), name="client_checkin"),
    path('report/', CheckinReportView.as_view(), name="checkin_report"),
]