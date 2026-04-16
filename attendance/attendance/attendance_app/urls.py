from django.urls import path
# from .views import AttendanceView
from attendance_app.views import *




urlpatterns = [
    # path('', AttendanceView.as_view()),   # /attendance/
    path('summary/', check_in_summary),
    path('check-out/', check_out),
    path('logs/', logs),
    path('working-hours/', working_hours),
    path('late-alerts/', late_alerts),
    path('report/', report_summary),
    path('export/', export_data),
    path('attendance-chart/', checkin_checkout_chart),
    path('away_logs/', away_logs),
    path('send-late-mail/', send_late_alert_mail),
    
]