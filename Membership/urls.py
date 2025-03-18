from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import register


urlpatterns = [
    path('',views.member_list, name="member_list"),
    path('member_card/<int:member_id>/',views.member_card, name="member_card"),
    path('member_card/<int:member_id>/edit',views.member_edit, name="member_edit"),
    path("login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", register, name="register"),

]