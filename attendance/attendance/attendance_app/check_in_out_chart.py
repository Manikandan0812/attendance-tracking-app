# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db import connection
# from datetime import datetime, timedelta

# from attendance_app.filters import build_common_filters
# # @api_view(['GET'])
# # def checkin_checkout_chart(request):
# #     try:
# #         # ==========================
# #         # GET FILTERS
# #         # ==========================
# #         date_str = request.GET.get('date')
# #         # zone = request.GET.get('zone')
# #         quick_time = request.GET.get('range')

# #         now = datetime.now()

# #         # ==========================
# #         # DATE BASE
# #         # ==========================
# #         if date_str:
# #             selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
# #         else:
# #             selected_date = now.date()

# #         start_day = datetime.combine(selected_date, datetime.min.time())

# #         # ==========================
# #         # TIME RANGE LOGIC
# #         # ==========================
# #         if quick_time == "Last 30 Minutes":
# #             start_time = now - timedelta(minutes=30)
# #             interval = 5

# #         elif quick_time == "Last 1 Hour":
# #             start_time = now - timedelta(hours=1)
# #             interval = 10

# #         elif quick_time == "Last 3 Hours":
# #             start_time = now - timedelta(hours=3)
# #             interval = 30

# #         else:  # Today (default)
# #             start_time = start_day
# #             interval = 60  # 1 hour

# #         end_time = now

# #         # ==========================
# #         # FILTERS
# #         # ==========================
# #         filters = "WHERE person_name != 'Unknown' AND attendance_date = %s"
# #         params = [selected_date]

# #         # if zone:
# #         #     filters += " AND assigned_shift_name = %s"
# #         #     params.append(zone)

# #         # ==========================
# #         # TABLE DATA
# #         # ==========================
# #         with connection.cursor() as cursor:
# #             cursor.execute(f"""
# #                 SELECT
# #                     id,
# #                     per_id,
# #                     person_name,
# #                     first_check_in,
# #                     last_check_out,
# #                     attendance_status
# #                 FROM attendance_aggre
# #                 {filters}
# #                 ORDER BY first_check_in
# #             """, params)

# #             cols = [c[0] for c in cursor.description]
# #             table_data = [dict(zip(cols, row)) for row in cursor.fetchall()]

# #         # ==========================
# #         # DYNAMIC CHART
# #         # ==========================
# #         chart_data = []

# #         current = start_time

# #         while current < end_time:
# #             next_slot = current + timedelta(minutes=interval)

# #             with connection.cursor() as cursor:
# #                 cursor.execute(f"""
# #                     SELECT
# #                         COUNT(*) FILTER (
# #                             WHERE first_check_in >= %s AND first_check_in < %s
# #                         ),
# #                         COUNT(*) FILTER (
# #                             WHERE last_check_out >= %s AND last_check_out < %s
# #                         )
# #                     FROM attendance_aggre
# #                     {filters}
# #                 """, [current, next_slot, current, next_slot] + params)

# #                 result = cursor.fetchone()

# #             chart_data.append({
# #                 "time": f"{current.strftime('%H:%M')} - {next_slot.strftime('%H:%M')}",
# #                 "checkin": result[0] or 0,
# #                 "checkout": result[1] or 0
# #             })

# #             current = next_slot

# #         # ==========================
# #         # SUMMARY KPI
# #         # ==========================
# #         with connection.cursor() as cursor:
# #             cursor.execute(f"""
# #                 SELECT
# #                     COUNT(*),
# #                     COUNT(*) FILTER (WHERE is_present = true),
# #                     COUNT(*) FILTER (WHERE is_absent = true),
# #                     COUNT(*) FILTER (WHERE is_late = true),
# #                     COUNT(*) FILTER (WHERE is_overtime = true)
# #                 FROM attendance_aggre
# #                 {filters}
# #             """, params)

# #             s = cursor.fetchone()

# #         summary = {
# #             "total": s[0],
# #             "present": s[1],
# #             "absent": s[2],
# #             "late": s[3],
# #             "overtime": s[4]
# #         }

# #         # ==========================
# #         # FINAL RESPONSE
# #         # ==========================
# #         return Response({
# #             "status": "success",
# #             "range": {
# #                 "start": str(start_time),
# #                 "end": str(end_time),
# #                 "interval_minutes": interval
# #             },
# #             "summary": summary,
# #             "chart": chart_data
# #         })

# #     except Exception as e:
# #         return Response({
# #             "status": "error",
# #             "message": str(e)
# #         })


# @api_view(['GET'])
# def checkin_checkout_chart(request):
#     try:
#         date = request.GET.get('date')
#         range_type = request.GET.get('range')

#         # ✅ FIXED UNPACK
#         where_sql, params, start_time, end_time = build_common_filters(date, range_type)

#         now = end_time

#         # ✅ INTERVAL
#         r = (range_type or "").lower()

#         if r in ["last 30 minutes", "last 30 mins"]:
#             interval = 5
#         elif r in ["last 1 hour", "last 1 hr"]:
#             interval = 10
#         elif r in ["last 3 hours", "last 3 hrs"]:
#             interval = 30
#         else:
#             interval = 60

#         if not start_time:
#             start_time = datetime.combine(now.date(), datetime.min.time())

#         chart_data = []
#         current = start_time

#         while current < now:
#             next_slot = current + timedelta(minutes=interval)

#             with connection.cursor() as cursor:
#                 cursor.execute(f"""SELECT
#                         COUNT(*) FILTER (
#                             WHERE first_check_in >= %s AND first_check_in < %s
#                         ),
#                         COUNT(*) FILTER (
#                             WHERE last_check_out >= %s AND last_check_out < %s
#                         )
#                     FROM attendance_aggre
#                     WHERE person_name != 'Unknown'
#                 """, [current, next_slot, current, next_slot])

#                 result = cursor.fetchone()

#             chart_data.append({
#                 "time": f"{current.strftime('%H:%M')} - {next_slot.strftime('%H:%M')}",
#                 "checkin": result[0] or 0,
#                 "checkout": result[1] or 0
#             })

#             current = next_slot

#         # ✅ SUMMARY
#         with connection.cursor() as cursor:
#             cursor.execute(f"""
#                 SELECT
#                     COUNT(*),
#                     COUNT(*) FILTER (WHERE is_present = true),
#                     COUNT(*) FILTER (WHERE is_absent = true),
#                     COUNT(*) FILTER (WHERE is_late = true),
#                     COUNT(*) FILTER (WHERE is_overtime = true)
#                 FROM attendance_aggre
#                 WHERE {where_sql}
#             """, params)

#             s = cursor.fetchone()

#         summary = {
#             "total": s[0],
#             "present": s[1],
#             "absent": s[2],
#             "late": s[3],
#             "overtime": s[4]
#         }

#         return Response({
#             "status": "success",
#             "range": {
#                 "start": str(start_time),
#                 "end": str(now),
#                 "interval_minutes": interval
#             },
#             "summary": summary,
#             "chart": chart_data
#         })

#     except Exception as e:
#         return Response({"status": "error", "message": str(e)})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from datetime import timedelta

from attendance_app.filters import build_common_filters

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
import json
from datetime import datetime


def parse_time_safe(time_str):
    try:
        if not time_str:
            return None
        if '.' in time_str:
            main, frac = time_str.split('.')
            frac = (frac + "000000")[:6]
            time_str = f"{main}.{frac}"
        return datetime.fromisoformat(time_str)
    except:
        return None


@api_view(['GET'])
def checkin_checkout_chart(request):
    try:
        query = """
        SELECT 
            person_name,
            attendance_date,
            all_check_in_images,
            all_check_out_images
        FROM attendance_aggre
        WHERE person_name != 'Unknown'
        ORDER BY attendance_date
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        date_map = {}

        for row in rows:
            person, date, checkins_json, checkouts_json = row

            try:
                checkins = json.loads(checkins_json or "[]")
                checkouts = json.loads(checkouts_json or "[]")
            except:
                checkins, checkouts = [], []

            date_str = str(date)

            if date_str not in date_map:
                date_map[date_str] = {
                    "date": date_str,
                    "events": []
                }

            # ✅ ADD CHECK-IN EVENTS
            for c in checkins:
                t = parse_time_safe(c.get("time"))
                if t:
                    date_map[date_str]["events"].append({
                        "type": "checkin",
                        "time": t.strftime("%H:%M"),
                        "person": person
                    })

            # ✅ ADD CHECK-OUT EVENTS
            for c in checkouts:
                t = parse_time_safe(c.get("time"))
                if t:
                    date_map[date_str]["events"].append({
                        "type": "checkout",
                        "time": t.strftime("%H:%M"),
                        "person": person
                    })

        # ✅ SORT EVENTS BY TIME
        final_data = []
        for d in date_map.values():
            d["events"].sort(key=lambda x: x["time"])
            final_data.append(d)

        return Response({
            "status": "success",
            "data": final_data
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        })