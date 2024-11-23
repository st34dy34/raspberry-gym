from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.member_list, name="member_list"),
    path('refresh-expiration/', views.refresh_expiration_dates, name='refresh_expiration'),
]