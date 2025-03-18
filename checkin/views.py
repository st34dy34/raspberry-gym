from django.shortcuts import render
from .models import CheckinCount
from django.utils import timezone
from datetime import timedelta

# Add a new view for reports
def checkin_report(request):
    # Get the last 7 days of data
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)
    
    checkins = CheckinCount.objects.filter(
        date__gte=start_date, 
        date__lte=end_date
    ).order_by('date')
    
    # Calculate weekly totals
    weekly_am_total = sum(checkin.am_checkins for checkin in checkins)
    weekly_pm_total = sum(checkin.pm_checkins for checkin in checkins)
    weekly_total = weekly_am_total + weekly_pm_total
    
    context = {
        'daily_checkins': checkins,
        'weekly_am_total': weekly_am_total,
        'weekly_pm_total': weekly_pm_total,
        'weekly_total': weekly_total,
        'start_date': start_date,
        'end_date': end_date
    }
    
    return render(request, 'checkin/report.html', context)

# Helper function to get or create today's check-in record
def get_today_checkin():
    today = timezone.now().date()
    return CheckinCount.objects.get_or_create(date=today)

# View to display the check-in page
def checkin_module(request):
    today_checkin, created = CheckinCount.objects.get_today()
    context = {
        'am_checkins': today_checkin.am_checkins,
        'pm_checkins': today_checkin.pm_checkins,
        'total_checkins': today_checkin.total_checkins,
    }
    return render(request, "checkin/checkin.html", context)

def client_checkin(request):
    if request.method != "POST":
        return render(request, 'checkin/checkin.html', {'error': 'Invalid request method'})
    
    try:
        today_checkin, created = CheckinCount.objects.get_today()
        
        current_time = timezone.now()
        time_slot = 'am' if current_time.hour < 12 else 'pm'
        
        if time_slot == 'am':
            today_checkin.am_checkins += 1
        else:
            today_checkin.pm_checkins += 1
            
        today_checkin.save()
        
        # Just pass the updated counts without a success message
        context = {
            'am_checkins': today_checkin.am_checkins,
            'pm_checkins': today_checkin.pm_checkins,
            'total_checkins': today_checkin.total_checkins,
            # Remove the success_message from here
        }
    except Exception as e:
        # Only show error if something goes wrong
        print(f"Error processing check-in: {e}")
        context = {
            'error': 'An error occurred while processing your check-in',
            'am_checkins': getattr(today_checkin, 'am_checkins', 0),
            'pm_checkins': getattr(today_checkin, 'pm_checkins', 0),
            'total_checkins': getattr(today_checkin, 'total_checkins', 0)
        }
    
    return render(request, 'checkin/checkin.html', context)

def members(request):
    # Placeholder view for members page
    return render(request, 'members.html')