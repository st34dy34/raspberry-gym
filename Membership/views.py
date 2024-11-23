from django.shortcuts import render
from .models import Member

# Create your views here.

def member_list(request):
    members = Member.objects.all()
    context = {
        'members':members,
    }
    return render(request,'Membership/members_layout.html',context)