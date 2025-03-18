from django.shortcuts import render
from .models import CheckinCount
from django.utils import timezone

# Helper function to get or create today's check-in record
def get_today_checkin():
    today = timezone.now().date()
    return CheckinCount.objects.get_or_create(date=today)

# View to display the check-in page
def checkin_module(request):
    today_checkin, created = get_today_checkin()  # Retrieve or create the check-in record
    context = {
        'am_checkins': today_checkin.am_checkins,
        'pm_checkins': today_checkin.pm_checkins,
        'total_checkins': today_checkin.total_checkins,
    }
    return render(request, "checkin/checkin.html", context)

# View to handle client check-ins
def client_checkin(request):
    today_checkin, created = get_today_checkin()  # Retrieve or create the check-in record

    if request.method == "POST":
        current_time = timezone.now()
        time_slot = 'am' if current_time.hour < 12 else 'pm'

        # Update the check-in count for AM or PM
        if time_slot == 'am':
            today_checkin.am_checkins += 1
        else:
            today_checkin.pm_checkins += 1

        today_checkin.save()  # Save the updated count

    # Prepare the context with the updated check-in counts
    context = {
        'am_checkins': today_checkin.am_checkins,
        'pm_checkins': today_checkin.pm_checkins,
        'total_checkins': today_checkin.total_checkins,
    }

    return render(request, 'checkin/checkin.html', context)
