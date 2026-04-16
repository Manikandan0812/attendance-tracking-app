from rest_framework.decorators import api_view
from rest_framework.response import Response
from attendance_app.db_utils import get_connection

@api_view(['GET'])
def late_alerts(request):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT per_id, alert_type, alert_message, created_at
        FROM alerts
        WHERE alert_type='Late'
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()

    data = []
    for r in rows:
        data.append({
            "per_id": r[0],
            "type": r[1],
            "message": r[2],
            "time": r[3]
        })

    cur.close()
    conn.close()

    return Response(data)