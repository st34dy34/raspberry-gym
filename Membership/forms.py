from django import forms
import datetime
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
        
        
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'membership_type', 'membership_duration', 'starting_date']

    # Validator that checks if selected type and value are same type (entry != 3 months, time != 10 entries)
    def clean(self):
        cleaned_data = super().clean()
        mtype = cleaned_data.get('membership_type')
        mduration = cleaned_data.get('membership_duration')

        vstupova = ['10 vstup', '20 vstup']
        casova = ['1 měsíc', '3 měsíce', '6 měsíců', '1 rok']

        if mtype == 'vstupová' and mduration not in vstupova:
            raise forms.ValidationError("Vstupová členství mohou mít pouze 10 nebo 20 vstupů.")
        elif mtype == 'časová' and mduration not in casova:
            raise forms.ValidationError("Časová členství mohou být 1, 3, 6 měsíců nebo 1 rok.")

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['starting_date'].initial = datetime.date.today()