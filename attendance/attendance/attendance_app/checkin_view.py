# # from rest_framework.decorators import api_view
# # from rest_framework.response import Response
# # from django.utils import timezone
# # from attendance_app.db_utils import get_connection

# # # @api_view(['POST'])
# # # def check_in(request):
# # #     per_id = request.data.get("per_id")
# # #     name = request.data.get("person_name", "Unknown")

# # #     conn = get_connection()
# # #     cur = conn.cursor()

# # #     cur.execute("""
# # #         INSERT INTO attendance (per_id, person_name, entry_time)
# # #         VALUES (%s, %s, %s)
# # #     """, (per_id, name, timezone.now()))

# # #     conn.commit()
# # #     cur.close()
# # #     conn.close()

# # #     return Response({"message": "Check-in success"})

# # # from django.http import JsonResponse
# # # from django.db import connection


# # # def check_in_summary(request):
# # #     try:
# # #         with connection.cursor() as cursor:

# # #             # Employee count
# # #             cursor.execute("""
# # #                 SELECT COUNT(DISTINCT per_id)
# # #                 FROM attendance_agg
# # #                 WHERE person_name != 'Unknown'
# # #             """)
# # #             employee_count = cursor.fetchone()[0]

# # #             # Total IN
# # #             cursor.execute("""
# # #                 SELECT COUNT(*)
# # #                 FROM attendance_raw
# # #                 WHERE event_type = 'IN'
# # #                 AND person_name != 'Unknown'
# # #             """)
# # #             total_checkins = cursor.fetchone()[0]

# # #             # Total OUT
# # #             cursor.execute("""
# # #                 SELECT COUNT(*)
# # #                 FROM attendance_raw
# # #                 WHERE event_type = 'OUT'
# # #                 AND person_name != 'Unknown'
# # #             """)
# # #             total_checkouts = cursor.fetchone()[0]

# # #             # Unknown
# # #             cursor.execute("""
# # #                 SELECT COUNT(*)
# # #                 FROM attendance_raw
# # #                 WHERE person_name = 'Unknown'
# # #             """)
# # #             unknown_entries = cursor.fetchone()[0]

# # #         return JsonResponse({
# # #             "status": "success",
# # #             "data": {
# # #                 "employee_count": employee_count,
# # #                 "total_checkins": total_checkins,
# # #                 "total_checkouts": total_checkouts,
# # #                 "unknown_entries": unknown_entries
# # #             }
# # #         })

# # #     except Exception as e:
# # #         return JsonResponse({
# # #             "status": "error",
# # #             "message": str(e)
# # #         })


# # from django.http import JsonResponse
# # from django.db import connection


# # # def check_in_summary(request):
# # #     try:
# # #         with connection.cursor() as cursor:

# # #             # ✅ Employee count (exclude TEMP + Unknown)
# # #             cursor.execute("""
# # #                 SELECT COUNT(DISTINCT per_id)
# # #                 FROM attendance_aggre
# # #                 WHERE person_name != 'Unknown'
# # #                 AND per_id NOT LIKE 'TEMP_%'
# # #             """)
# # #             employee_count = cursor.fetchone()[0]

# # #             cursor.execute("""
# # #                 SELECT COALESCE(SUM(total_check_ins), 0)
# # #                 FROM (
# # #                     SELECT per_id, MAX(total_check_ins) AS total_check_ins
# # #                     FROM attendance_aggre
# # #                     WHERE person_name != 'Unknown'
# # #                     AND per_id NOT LIKE 'TEMP_%'
# # #                     GROUP BY per_id
# # #                 ) t
# # #             """)
# # #             total_checkins = cursor.fetchone()[0]


# # #             cursor.execute("""
# # #                 SELECT COALESCE(SUM(total_check_outs), 0)
# # #                 FROM (
# # #                     SELECT per_id, MAX(total_check_outs) AS total_check_outs
# # #                     FROM attendance_aggre
# # #                     WHERE person_name != 'Unknown'
# # #                     AND per_id NOT LIKE 'TEMP_%'
# # #                     GROUP BY per_id
# # #                 ) t
# # #             """)
# # #             total_checkouts = cursor.fetchone()[0]

# # #             # ✅ Unknown / TEMP entries
# # #             cursor.execute("""
# # #                 SELECT COUNT(*)
# # #                 FROM attendance_aggre
# # #                 WHERE person_name = 'Unknown'
# # #                 OR per_id LIKE 'TEMP_%'
# # #             """)
# # #             unknown_entries = cursor.fetchone()[0]

# # #         return JsonResponse({
# # #             "status": "success",
# # #             "data": {
# # #                 "employee_count": employee_count,
# # #                 "total_checkins": total_checkins,
# # #                 "total_checkouts": total_checkouts,
# # #                 "unknown_entries": unknown_entries
# # #             }
# # #         })

# # #     except Exception as e:
# # #         return JsonResponse({
# # #             "status": "error",
# # #             "message": str(e)
# # #         })


# # # from django.http import JsonResponse
# # # from django.db import connection

# # # def check_in_summary(request):
# # #     try:
# # #         date = request.GET.get("date")

# # #         print("Received date:", date)

# # #         # ✅ SAFE FILTER BUILD
# # #         if date:
# # #             where_clause = "AND attendance_date = %s"
# # #             params = [date]
# # #         else:
# # #             where_clause = ""
# # #             params = []

# # #         def execute_query(query):
# # #             with connection.cursor() as cursor:
# # #                 if params:
# # #                     cursor.execute(query, params)
# # #                 else:
# # #                     cursor.execute(query)
# # #                 return cursor.fetchone()[0] or 0

# # #         # ✅ Employee count
# # #         employee_count = execute_query(f"""
# # #             SELECT COUNT(DISTINCT per_id)
# # #             FROM attendance_aggre
# # #             WHERE person_name != 'Unknown'
# # #             AND per_id NOT LIKE 'TEMP_%'
# # #             {where_clause}
# # #         """)

# # #         # ✅ Total checkins
# # #         total_checkins = execute_query(f"""
# # #             SELECT COALESCE(SUM(total_check_ins), 0)
# # #             FROM (
# # #                 SELECT per_id, MAX(total_check_ins) AS total_check_ins
# # #                 FROM attendance_aggre
# # #                 WHERE person_name != 'Unknown'
# # #                 AND per_id NOT LIKE 'TEMP_%'
# # #                 {where_clause}
# # #                 GROUP BY per_id
# # #             ) t
# # #         """)

# # #         # ✅ Total checkouts
# # #         total_checkouts = execute_query(f"""
# # #             SELECT COALESCE(SUM(total_check_outs), 0)
# # #             FROM (
# # #                 SELECT per_id, MAX(total_check_outs) AS total_check_outs
# # #                 FROM attendance_aggre
# # #                 WHERE person_name != 'Unknown'
# # #                 AND per_id NOT LIKE 'TEMP_%'
# # #                 {where_clause}
# # #                 GROUP BY per_id
# # #             ) t
# # #         """)

# # #         # ✅ Unknown entries
# # #         unknown_entries = execute_query(f"""
# # #             SELECT COUNT(*)
# # #             FROM attendance_aggre
# # #             WHERE (
# # #                 person_name = 'Unknown'
# # #                 OR per_id LIKE 'TEMP_%'
# # #             )
# # #             {where_clause}
# # #         """)

# # #         return JsonResponse({
# # #             "status": "success",
# # #             "data": {
# # #                 "employee_count": employee_count,
# # #                 "total_checkins": total_checkins,
# # #                 "total_checkouts": total_checkouts,
# # #                 "unknown_entries": unknown_entries
# # #             }
# # #         })

# # #     except Exception as e:
# # #         import traceback
# # #         traceback.print_exc()

# # #         return JsonResponse({
# # #             "status": "error",
# # #             "message": str(e)
# # #         }, status=500)

# # #date working code
# # # from rest_framework.decorators import api_view
# # # from rest_framework.response import Response
# # # from django.db import connection

# # # @api_view(['GET'])
# # # def check_in_summary(request):
# # #     try:
# # #         date = request.GET.get('date')

# # #         where_conditions = ["person_name != 'Unknown'"]
# # #         params = []

# # #         # ✅ DATE FILTER
# # #         if date:
# # #             where_conditions.append("DATE(attendance_date) = %s")
# # #             params.append(date)

# # #         where_sql = " AND ".join(where_conditions)
        

# # #         query = f"""
# # #             SELECT 
# # #                 COUNT(DISTINCT per_id),
# # #                 COALESCE(SUM(total_check_ins),0),
# # #                 COALESCE(SUM(total_check_outs),0),
# # #                 COUNT(*) FILTER (WHERE person_name = 'Unknown')
# # #             FROM attendance_aggre
# # #             WHERE {where_sql}
# # #         """
# # #         # print("QUERY:", query)
# # #         # print("PARAMS:", params)        
# # #         with connection.cursor() as cursor:
# # #             cursor.execute(query, params)   # ✅ params MATCHES %s
# # #             row = cursor.fetchone()

# # #         return Response({
# # #             "status": "success",
# # #             "data": {
# # #                 "employee_count": row[0],
# # #                 "total_checkins": row[1],
# # #                 "total_checkouts": row[2],
# # #                 "unknown_entries": row[3]
# # #             }
# # #         })

# # #     except Exception as e:
# # #         print("ERROR:", str(e))  # 🔥 debug log
# # #         return Response({
# # #             "status": "error",
# # #             "message": str(e)
# # #         })


# # from rest_framework.decorators import api_view
# # from rest_framework.response import Response
# # from django.db import connection
# # from datetime import timedelta
# # from django.utils.timezone import now
# # from attendance_app.filters import build_common_filters

# # @api_view(['GET'])
# # def check_in_summary(request):
# #     try:
# #         date = request.GET.get('date')
# #         range_type = request.GET.get('range')

# #         # ✅ FIXED UNPACK
# #         where_sql, params, start_time, end_time = build_common_filters(date, range_type)

# #         query = f"""
# #         SELECT 
# #             COUNT(DISTINCT CASE WHEN person_name != 'Unknown' THEN per_id END),
# #             COUNT(DISTINCT CASE WHEN person_name != 'Unknown' AND first_check_in IS NOT NULL THEN per_id END),
# #             COUNT(DISTINCT CASE WHEN person_name != 'Unknown' AND last_check_out IS NOT NULL THEN per_id END),
# #             COUNT(*) FILTER (WHERE person_name = 'Unknown')
# #         FROM attendance_aggre
# #         WHERE {where_sql}
# #         """

# #         with connection.cursor() as cursor:
# #             cursor.execute(query, params)
# #             row = cursor.fetchone()

# #         return Response({
# #             "status": "success",
# #             "data": {
# #                 "employee_count": row[0] or 0,
# #                 "total_checkins": row[1] or 0,
# #                 "total_checkouts": row[2] or 0,
# #                 "unknown_entries": row[3] or 0
# #             }
# #         })

# #     except Exception as e:
# #         return Response({"status": "error", "message": str(e)})

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db import connection

# from attendance_app.filters import build_common_filters

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db import connection


# @api_view(['GET'])
# def check_in_summary(request):
#     try:
#         query = """
#         WITH first_in AS (
#             SELECT 
#                 per_id,
#                 attendance_date,
#                 MIN(first_check_in) AS first_check_in
#             FROM attendance_aggre
#             WHERE first_check_in IS NOT NULL
#               AND person_name <> 'Unknown'
#             GROUP BY per_id, attendance_date
#         ),

#         base_events AS (

#             -- FIRST CHECK-IN
#             SELECT 
#                 ag.attendance_date,
#                 ag.first_check_in AS time,
#                 ag.person_name,
#                 'FIRST_IN' AS type
#             FROM attendance_aggre ag
#             JOIN first_in fi
#               ON ag.per_id = fi.per_id
#              AND ag.attendance_date = fi.attendance_date
#              AND ag.first_check_in = fi.first_check_in
#             WHERE ag.person_name <> 'Unknown'
#               AND ag.first_check_in IS NOT NULL

#             UNION ALL

#             -- MULTI CHECK-IN
#             SELECT 
#                 ag.attendance_date,
#                 ag.first_check_in AS time,
#                 ag.person_name,
#                 'MULTI_IN' AS type
#             FROM attendance_aggre ag
#             JOIN first_in fi
#               ON ag.per_id = fi.per_id
#              AND ag.attendance_date = fi.attendance_date
#             WHERE ag.first_check_in IS NOT NULL
#               AND ag.first_check_in > fi.first_check_in
#               AND ag.person_name <> 'Unknown'

#             UNION ALL

#             -- FIRST CHECK-OUT
#             SELECT 
#                 ag.attendance_date,
#                 ag.last_check_out AS time,
#                 ag.person_name,
#                 'FIRST_OUT' AS type
#             FROM attendance_aggre ag
#             WHERE ag.last_check_out IS NOT NULL
#               AND ag.person_name <> 'Unknown'
#               AND ag.last_check_out = (
#                   SELECT MIN(ag2.last_check_out)
#                   FROM attendance_aggre ag2
#                   WHERE ag2.per_id = ag.per_id
#                     AND ag2.attendance_date = ag.attendance_date
#                     AND ag2.last_check_out IS NOT NULL
#               )

#             UNION ALL

#             -- MULTI CHECK-OUT
#             SELECT 
#                 ag.attendance_date,
#                 ag.last_check_out AS time,
#                 ag.person_name,
#                 'MULTI_OUT' AS type
#             FROM attendance_aggre ag
#             WHERE ag.last_check_out IS NOT NULL
#               AND ag.person_name <> 'Unknown'
#               AND ag.last_check_out > (
#                   SELECT MIN(ag2.last_check_out)
#                   FROM attendance_aggre ag2
#                   WHERE ag2.per_id = ag.per_id
#                     AND ag2.attendance_date = ag.attendance_date
#                     AND ag2.last_check_out IS NOT NULL
#               )
#         ),

#         emp_count AS (
#             SELECT 
#                 attendance_date,
#                 COUNT(DISTINCT per_id) AS employee_count
#             FROM attendance_aggre
#             WHERE person_name <> 'Unknown'
#               AND first_check_in IS NOT NULL
#             GROUP BY attendance_date
#         )

#         SELECT 
#             b.attendance_date,
#             b.time,
#             b.person_name,
#             b.type,
#             e.employee_count
#         FROM base_events b
#         LEFT JOIN emp_count e 
#           ON b.attendance_date = e.attendance_date
#         ORDER BY b.attendance_date DESC, b.time ASC;
#         """

#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             columns = [col[0] for col in cursor.description]
#             rows = cursor.fetchall()

#         grouped = {}

#         for row in rows:
#             record = dict(zip(columns, row))
#             date = str(record["attendance_date"])
#             event_type = record["type"]

#             if date not in grouped:
#                 grouped[date] = {
#                     "attendance_date": date,
#                     "employee_count": record["employee_count"],
#                     "all_check_in": 0,
#                     "all_check_out": 0,
#                     "unknown_count": 0,
#                     "events": []
#                 }

#             time_val = record["time"]
#             if time_val:
#                 time_val = time_val.strftime("%Y-%m-%d %H:%M:%S")

#             is_checkin = event_type in ["FIRST_IN", "MULTI_IN"]
#             is_checkout = event_type in ["FIRST_OUT", "MULTI_OUT"]

#             grouped[date]["events"].append({
#                 "time": time_val,
#                 "checkin_count": 1 if is_checkin else 0,
#                 "checkout_count": 1 if is_checkout else 0,
#                 "unknown_count": 1 if record["person_name"] == "Unknown" else 0,
#                 "first_check_in": 1 if event_type == "FIRST_IN" else 0
#             })

#         # 🔥 FINAL AGGREGATION PER DAY
#         for date in grouped:
#             grouped[date]["all_check_in"] = sum(e["checkin_count"] for e in grouped[date]["events"])
#             grouped[date]["all_check_out"] = sum(e["checkout_count"] for e in grouped[date]["events"])
#             grouped[date]["unknown_count"] = sum(e["unknown_count"] for e in grouped[date]["events"])
#             grouped[date]["employee_count"] = grouped[date]["employee_count"] or 0

#         return Response({
#             "status": "success",
#             "data": list(grouped.values())
#         })

#     except Exception as e:
#         return Response({
#             "status": "error",
#             "message": str(e)
#         })

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db import connection


# @api_view(['GET'])
# def check_in_summary(request):
#     try:

#         query = """
#         WITH employee_data AS (
#             SELECT
#                 attendance_date,
#                 COUNT(*) FILTER (
#                     WHERE person_name <> 'Unknown'
#                     AND first_check_in IS NOT NULL
#                 ) AS employee_count,

#                 COUNT(*) FILTER (
#                     WHERE person_name = 'Unknown'
#                 ) AS unknown_count
#             FROM attendance_aggre
#             GROUP BY attendance_date
#         ),

#         checkin_data AS (
#             SELECT
#                 attendance_date,
#                 COUNT(elem->>'time') AS all_check_in
#             FROM attendance_aggre,
#             LATERAL jsonb_array_elements(all_check_in_images::jsonb) elem
#             WHERE person_name <> 'Unknown'
#             GROUP BY attendance_date
#         ),

#         checkout_data AS (
#             SELECT
#                 attendance_date,
#                 COUNT(elem->>'time') AS all_check_out
#             FROM attendance_aggre,
#             LATERAL jsonb_array_elements(all_check_out_images::jsonb) elem
#             WHERE person_name <> 'Unknown'
#             GROUP BY attendance_date
#         )

#         SELECT
#             e.attendance_date,
#             COALESCE(e.employee_count, 0) AS employee_count,
#             COALESCE(ci.all_check_in, 0) AS all_check_in,
#             COALESCE(co.all_check_out, 0) AS all_check_out,
#             COALESCE(e.unknown_count, 0) AS unknown_count
#         FROM employee_data e
#         LEFT JOIN checkin_data ci ON e.attendance_date = ci.attendance_date
#         LEFT JOIN checkout_data co ON e.attendance_date = co.attendance_date
#         ORDER BY e.attendance_date DESC;
#         """

#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             rows = cursor.fetchall()

#         data = []
#         for row in rows:
#             data.append({
#                 "attendance_date": row[0],
#                 "employee_count": row[1],
#                 "all_check_in": row[2],
#                 "all_check_out": row[3],
#                 "unknown_count": row[4],
#                 "events": []   # optional: fill later
#             })

#         return Response({
#             "status": "success",
#             "data": data
#         })

#     except Exception as e:
#         return Response({
#             "status": "error",
#             "message": str(e)
#         }, status=500)

# 

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection


@api_view(['GET'])
def check_in_summary(request):
    try:

        query = """
        WITH employee_data AS (
            SELECT
                attendance_date,

                COUNT(*) FILTER (
                    WHERE person_name <> 'Unknown'
                    AND first_check_in IS NOT NULL
                ) AS employee_count,

                COUNT(*) FILTER (
                    WHERE person_name <> 'Unknown'
                    AND first_check_in IS NOT NULL
                ) AS first_checkin_count

            FROM attendance_aggre
            GROUP BY attendance_date
        ),

        checkins AS (
            SELECT
                a.attendance_date,
                (elem->>'time')::timestamp AS event_time,
                1 AS checkin_count,
                0 AS checkout_count,
                0 AS unknown_count,

                CASE
                    WHEN (elem->>'time')::timestamp = a.first_check_in
                    THEN 1 ELSE 0
                END AS first_checkin_count

            FROM attendance_aggre a,
            LATERAL jsonb_array_elements(a.all_check_in_images::jsonb) elem
            WHERE a.person_name <> 'Unknown'
        ),

        checkouts AS (
            SELECT
                a.attendance_date,
                (elem->>'time')::timestamp AS event_time,
                0 AS checkin_count,
                1 AS checkout_count,
                0 AS unknown_count,
                0 AS first_checkin_count
            FROM attendance_aggre a,
            LATERAL jsonb_array_elements(a.all_check_out_images::jsonb) elem
            WHERE a.person_name <> 'Unknown'
        ),

        unknowns AS (
            SELECT
                attendance_date,
                first_check_in AS event_time,
                0 AS checkin_count,
                0 AS checkout_count,
                1 AS unknown_count,
                0 AS first_checkin_count
            FROM attendance_aggre
            WHERE person_name = 'Unknown'
              AND first_check_in IS NOT NULL
        ),

        all_events AS (
            SELECT attendance_date, event_time, checkin_count, checkout_count, unknown_count, first_checkin_count FROM checkins
            UNION ALL
            SELECT attendance_date, event_time, checkin_count, checkout_count, unknown_count, first_checkin_count FROM checkouts
            UNION ALL
            SELECT attendance_date, event_time, checkin_count, checkout_count, unknown_count, first_checkin_count FROM unknowns
        ),

        aggregated_events AS (
            SELECT
                attendance_date,
                event_time,
                SUM(checkin_count) AS checkin_count,
                SUM(checkout_count) AS checkout_count,
                SUM(unknown_count) AS unknown_count,
                SUM(first_checkin_count) AS first_checkin_count
            FROM all_events
            GROUP BY attendance_date, event_time
        )

        SELECT
            e.attendance_date,
            e.employee_count,
            e.first_checkin_count,
            ae.event_time,
            ae.checkin_count,
            ae.checkout_count,
            ae.unknown_count,
            ae.first_checkin_count
        FROM employee_data e
        LEFT JOIN aggregated_events ae
            ON e.attendance_date = ae.attendance_date
        ORDER BY e.attendance_date DESC, ae.event_time ASC;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        result_map = {}

        for row in rows:
            date = str(row[0])

            if date not in result_map:
                result_map[date] = {
                    "attendance_date": date,
                    "employee_count": row[1],
                    "first_checkin_count": row[2],
                    "events": []
                }

            if row[3] is not None:
                result_map[date]["events"].append({
                    "time": row[3].strftime("%Y-%m-%d %H:%M:%S"),
                    "checkin_count": row[4],
                    "checkout_count": row[5],
                    "unknown_count": row[6],
                    "first_checkin_count": row[7]
                })

        return Response({
            "status": "success",
            "data": list(result_map.values())
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)
    