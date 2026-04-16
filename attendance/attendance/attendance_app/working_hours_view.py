from rest_framework.decorators import api_view
from rest_framework.response import Response
from attendance_app.db_utils import get_connection

@api_view(['GET'])
def working_hours(request):
    per_id = request.GET.get("per_id")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT SUM(total_hours)
        FROM attendance_aggregate
        WHERE per_id=%s
    """, (per_id,))

    total = cur.fetchone()[0] or 0

    cur.close()
    conn.close()

    return Response({
        "per_id": per_id,
        "total_hours": round(total, 2)
    })