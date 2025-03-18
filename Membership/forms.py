from django import forms
from .models import Member
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MemberEditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'membership_type', 'membership_duration', 'starting_date',  'expiration_date', 'expired']
    
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]