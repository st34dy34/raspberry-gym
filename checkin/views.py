from django.shortcuts import render, redirect
from django.views import View
from .models import CheckinCount
from django.utils import timezone
from datetime import timedelta
from django.views.generic import TemplateView
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin



class CheckinReportView(LoginRequiredMixin,TemplateView):
    template_name = "checkin/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=6)
        
        checkins = CheckinCount.objects.filter(
            date__gte=start_date, 
            date__lte=end_date
        ).order_by('date')
        
        # Use aggregation to calculate totals
        weekly_totals = checkins.aggregate(
            weekly_am_total=Sum('am_checkins'),
            weekly_pm_total=Sum('pm_checkins'),
            weekly_total=Sum('total_checkins')
        )
        
        context.update({
            'daily_checkins': checkins,
            'weekly_am_total': weekly_totals['weekly_am_total'] or 0,
            'weekly_pm_total': weekly_totals['weekly_pm_total'] or 0,
            'weekly_total': weekly_totals['weekly_total'] or 0,
            'start_date': start_date,
            'end_date': end_date
        })
        return context

class CheckinModuleView(LoginRequiredMixin,TemplateView):
    template_name = "checkin/checkin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today_checkin, created = CheckinCount.objects.get_today()
        context.update({
            'am_checkins': today_checkin.am_checkins,
            'pm_checkins': today_checkin.pm_checkins,
            'total_checkins': today_checkin.total_checkins,
        })
        return context

class ClientCheckinView(LoginRequiredMixin,View):
    def post(self, request):
        try:
            today_checkin, created = CheckinCount.objects.get_today()
            current_time = timezone.now()
            time_slot = 'am' if current_time.hour < 12 else 'pm'
            
            if time_slot == 'am':
                today_checkin.am_checkins += 1
            else:
                today_checkin.pm_checkins += 1
                
            today_checkin.save()
            
            # Redirect to the check-in page to avoid form resubmission
            return redirect('checkin_module')
        
        except Exception as e:
            print(f"Error processing check-in: {e}")
            context = {
                'error': 'An error occurred while processing your check-in',
                'am_checkins': getattr(today_checkin, 'am_checkins', 0),
                'pm_checkins': getattr(today_checkin, 'pm_checkins', 0),
                'total_checkins': getattr(today_checkin, 'total_checkins', 0)
            }
            return render(request, 'checkin/checkin.html', context)