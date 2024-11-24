from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.member_list, name="member_list"),
    path('member_card/<int:member_id>/',views.member_card, name="member_card"),
    path('member_card/<int:member_id>/edit',views.member_edit, name="member_edit"),
]