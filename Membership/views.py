from django.shortcuts import render
from .models import Member

# Create your views here.

def member_list(request):
    membership_type = request.GET.get('membership_type')  # Get the filter parameter
    if membership_type:
         members = Member.objects.filter(membership_type=membership_type)
    else:
        members = Member.objects.all()
    context = {
        'members':members,
    }
    return render(request,'Membership/members_layout.html',context)