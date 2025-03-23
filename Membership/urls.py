from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, add_member, ExportMembersCSV


urlpatterns = [
    path('',views.member_list, name="member_list"),
    path('members_add/', add_member, name='member_add'),
    path('member_card/<int:member_id>/',views.member_card, name="member_card"),
    path('member_card/<int:member_id>/edit',views.member_edit, name="member_edit"),
    path("login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", register, name="register"),
    path('members/export/', ExportMembersCSV.as_view(), name='export_members'),

]