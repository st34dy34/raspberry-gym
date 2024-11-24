from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.checkin_module, name="checkin_module"),
]