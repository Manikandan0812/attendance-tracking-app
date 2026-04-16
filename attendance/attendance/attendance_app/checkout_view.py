from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from attendance_app.db_utils import get_connection

@api_view(['POST'])
def check_out(request):
    per_id = request.data.get("per_id")

    conn = get_connection()
    cur = conn.cursor()

    # Get last check-in
    cur.execute("""
        SELECT id, entry_time FROM attendance
        WHERE per_id=%s AND exit_time IS NULL
        ORDER BY id DESC LIMIT 1
    """, (per_id,))
    
    row = cur.fetchone()

    if not row:
        return Response({"error": "No check-in found"})

    raw_id, entry_time = row
    exit_time = timezone.now()

    # Update exit
    cur.execute("""
        UPDATE attendance_raw
        SET exit_time=%s
        WHERE id=%s
    """, (exit_time, raw_id))

    # Calculate hours
    total_seconds = (exit_time - entry_time).total_seconds()
    hours = round(total_seconds / 3600, 2)

    work_date = entry_time.date()

    # Insert aggregate
    cur.execute("""
        INSERT INTO attendance_aggregate (per_id, work_date, total_hours, status)
        VALUES (%s, %s, %s, %s)
    """, (per_id, work_date, hours, "Present"))

    # Late alert
    if entry_time.hour >= 10:
        cur.execute("""
            INSERT INTO alerts (per_id, alert_type, alert_message)
            VALUES (%s, %s, %s)
        """, (per_id, "Late", "User checked in late"))

    conn.commit()
    cur.close()
    conn.close()

    return Response({
        "message": "Check-out success",
        "working_hours": hours
    })