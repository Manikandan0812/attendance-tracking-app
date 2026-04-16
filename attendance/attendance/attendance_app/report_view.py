from rest_framework.decorators import api_view
from rest_framework.response import Response
from attendance_app.db_utils import get_connection

@api_view(['GET'])
def report_summary(request):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM attendance_aggregate")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM attendance_aggregate WHERE status='Present'")
    present = cur.fetchone()[0]

    absent = total - present

    cur.close()
    conn.close()

    return Response({
        "total": total,
        "present": present,
        "absent": absent
    })