from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Member
from .forms import MemberEditForm 

# Create your views here.

def member_list(request):
    membership_type = request.GET.get('membership_type')  
    membership_duration = request.GET.get('membership_duration')  
    search_query = request.GET.get('search', '') 
    if membership_type:
         members = Member.objects.filter(membership_type=membership_type)
    elif membership_duration:
         members = Member.objects.filter(membership_duration=membership_duration)
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



def member_card(request,member_id):
    member = get_object_or_404(Member,id=member_id)
    context = {
        'member':member,
    }
    return render(request,'Membership/member_card.html',context)



def member_edit(request,member_id):
    member = get_object_or_404(Member,id=member_id)
    
    if request.method == "POST":  # If form is posted do this
        form = MemberEditForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            print(form)
            return redirect('member_card', member_id=member.id)
    else:
        form = MemberEditForm(instance=member)  # else Pre-fill the form with the current member data
        
        
    context = {
        'member': member,
        'form': form,
    }
    return render(request,'Membership/member_edit.html',context)