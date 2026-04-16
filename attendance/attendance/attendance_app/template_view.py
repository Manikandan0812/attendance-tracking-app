# from django.shortcuts import render
# from .models import AttendanceEvent, AttendanceSummary, AttendanceAlert

# def view_dashboard(request):
#     events = AttendanceEvent.objects.all().order_by('-event_time')
#     summary = AttendanceSummary.objects.all()
#     alerts = AttendanceAlert.objects.all().order_by('-alert_time')

#     return render(request, 'view.html', {
#         'events': events,
#         'summary': summary,
#         'alerts': alerts
#     })