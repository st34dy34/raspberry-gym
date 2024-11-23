from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Member

# Create your views here.

def member_list(request):
    membership_type = request.GET.get('membership_type')  # Get the filter parameter
    search_query = request.GET.get('search', '') # search bar
    if membership_type:
         members = Member.objects.filter(membership_type=membership_type)
    elif search_query:
         # Use Q to filter on first_name or last_name (since full_name is not a database field)
        members = Member.objects.filter(
            Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
        )
    else:
        members = Member.objects.all()
        
    members = members.order_by('-id')
    context = {
        'members':members,
    }
    return render(request,'Membership/members_layout.html',context)

def refresh_expiration_dates(request):
    members = Member.objects.all()
    for member in members:
        member.expiration_date = member.calculate_expiration()
        member.save()  
        
    return redirect('member_list') 