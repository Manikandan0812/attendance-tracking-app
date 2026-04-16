from rest_framework.decorators import api_view
from rest_framework.response import Response
from attendance_app.db_utils import get_connection

@api_view(['GET'])
def export_data(request):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT per_id, work_date, total_hours, status
        FROM attendance_aggregate
        ORDER BY work_date DESC
    """)

    rows = cur.fetchall()

    data = []
    for r in rows:
        data.append({
            "per_id": r[0],
            "date": r[1],
            "hours": r[2],
            "status": r[3]
        })

    cur.close()
    conn.close()

    return Response(data)