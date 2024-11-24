from django import forms
from .models import Member

class MemberEditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'membership_type', 'membership_duration', 'starting_date',  'expiration_date', 'expired']
    