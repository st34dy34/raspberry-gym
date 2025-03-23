from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils.timezone import now
from .models import Member
from .forms import MemberEditForm 
from .forms import UserRegisterForm
from .forms import MemberForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.views import View
import csv

# Create your views here.

@login_required
def member_list(request):
    membership_type = request.GET.get('membership_type')  
    membership_duration = request.GET.get('membership_duration')  
    search_query = request.GET.get('search', '') 
    #-------------QUERY-----------#
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
    #-------------UPDATE EXPIRY-----------#
    for member in members:
        if member.membership_type == "časová" and member.starting_date and member.membership_duration:
            # Call the method to calculate expiration and save
            member.calculate_expiration()
            if member.expiration_date:  # Check if expiration_date is not None
                member.expired = member.expiration_date < now().date()  # Update expired status
            else:
                member.expired = True  # If expiration_date is None, consider it expired
            member.save()
            
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

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect("member_list")  # Redirect to member list after registration
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Člen byl úspěšně přidán.')
            return redirect('member_list')
        else:
            messages.error(request, 'Formulář obsahuje chyby.')
    else:
        form = MemberForm()
    return render(request, 'Membership/member_add.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ExportMembersCSV(View):
    def get(self, request):
        # Adding BOM encoding for Excel
        response = HttpResponse(
            content_type='text/csv; charset=utf-8-sig'
        )
        response['Content-Disposition'] = 'attachment; filename="members.csv"'

        # BOM = \ufeff
        response.write('\ufeff')

        writer = csv.writer(response, delimiter=';')
        writer.writerow(['Jméno', 'Příjmení', 'Typ členství', 'Délka', 'Od', 'Do', 'Expirováno'])

        for member in Member.objects.all():
            writer.writerow([
                member.first_name,
                member.last_name,
                member.membership_type,
                member.membership_duration,
                member.starting_date,
                member.expiration_date,
                'Ano' if member.expired else 'Ne'
            ])

        return response