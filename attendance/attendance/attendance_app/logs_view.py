# # from rest_framework.decorators import api_view
# # from rest_framework.response import Response
# # from django.db import connection

# # @api_view(['GET'])
# # def logs(request):
# #     try:
# #         with connection.cursor() as cursor:
# #             cursor.execute("""
# #                 SELECT *
# #                 FROM attendance_aggre
# #                 WHERE person_name != 'Unknown'
                
# #             """)
# #             columns = [col[0] for col in cursor.description]
# #             rows = cursor.fetchall()

# #         data = [dict(zip(columns, row)) for row in rows]

# #         return Response({
# #             "status": "success",
# #             "data": data
# #         })

# #     except Exception as e:
# #         return Response({
# #             "status": "error",
# #             "message": str(e)
# #         })


# # SELECT *
# #                 FROM attendance_raw
# #                 WHERE person_name != 'Unknown'
# #                 ORDER BY event_time ASC


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db import connection

# # @api_view(['GET'])
# # def logs(request):
# #     try:
# #         with connection.cursor() as cursor:
# #             cursor.execute("""
# #                 SELECT *
# #                 FROM attendance_aggre
# #                 WHERE person_name != 'Unknown'
                
# #             """)
# #             columns = [col[0] for col in cursor.description]
# #             rows = cursor.fetchall()

# #         data = [dict(zip(columns, row)) for row in rows]

# #         return Response({
# #             "status": "success",
# #             "data": data
# #         })

# #     except Exception as e:
# #         return Response({
# #             "status": "error",
# #             "message": str(e)
# #         })


# # # SELECT *
# # #                 FROM attendance_raw
# # #                 WHERE person_name != 'Unknown'
# # #                 ORDER BY event_time ASC


# # from rest_framework.decorators import api_view
# # from rest_framework.response import Response
# # from django.db import connection

# # @api_view(['GET'])
# # def logs(request):
# #     try:
# #         with connection.cursor() as cursor:
# #             cursor.execute("""
# #                     SELECT *,
# #                         CASE 
# #                             WHEN last_check_out IS NULL THEN NULL
# #                             WHEN first_check_in > last_check_out THEN NULL
# #                             ELSE last_check_out
# #                         END AS last_checkout_fixed
# #                     FROM attendance_aggre
# #                     WHERE person_name != 'Unknown'
# #                     ORDER BY attendance_date DESC;
# #             """)

# #             columns = [col[0] for col in cursor.description]
# #             rows = cursor.fetchall()

# #         data = []
# #         for row in rows:
# #             record = dict(zip(columns, row))

# #             data.append({
# #                 "emp_id": record["per_id"],
# #                 "name": record["person_name"],
# #                 "date": record["date"],
# #                 "first_checkin": record["first_checkin"],
# #                 "last_checkout": record["last_checkout"],
# #                 "status": "IN" if record["last_checkout"] is None else "OUT"
# #             })

# #         return Response({
# #             "status": "success",
# #             "data": data
# #         })

# #     except Exception as e:
# #         return Response({
# #             "status": "error",
# #             "message": str(e)
# #         })
# MEDIA_URL = '/media/'
# MEDIA_ROOT = r'D:\Vision Analytics\Face_recog\evidence_images'

# from django.db import connection
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# import os
# from attendance_app.filters import build_common_filters

# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# import os

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db import connection
# import os

# # @api_view(['GET'])
# # def logs(request):
# #     try:
# #         date = request.GET.get('date')
# #         range_type = request.GET.get('range')

# #         where_sql, params = build_common_filters(date, range_type)

# #         query = f"""
# #             SELECT 
# #                 ag.id,
# #                 ag.per_id,
# #                 ag.person_name,
# #                 ag.attendance_date,
# #                 ag.first_check_in,

# #                 CASE 
# #                     WHEN ag.last_check_out IS NULL THEN NULL
# #                     WHEN ag.first_check_in > ag.last_check_out THEN NULL
# #                     ELSE ag.last_check_out
# #                 END AS last_checkout,

# #                 CASE 
# #                     WHEN ag.last_check_out IS NULL THEN NULL
# #                     WHEN ag.first_check_in > ag.last_check_out THEN NULL
# #                     ELSE ag.last_check_out_image
# #                 END AS last_check_out_image,

# #                 ag.total_check_ins,
# #                 ag.total_check_outs,
# #                 ag.attendance_status,
# #                 ag.first_check_in_image,

# #                 -- Shift details
# #                 ps.shift_name

# #             FROM attendance_aggre ag
# #             LEFT JOIN person_shift ps 
# #                 ON ag.per_id = ps.per_id

# #             WHERE ag.person_name != 'Unknown'
# #               AND {where_sql}

# #             ORDER BY ag.attendance_date DESC, ag.first_check_in ASC NULLS LAST
# #         """

# #         with connection.cursor() as cursor:
# #             cursor.execute(query, params)
# #             columns = [col[0] for col in cursor.description]
# #             rows = cursor.fetchall()

# #         data = []
# #         for row in rows:
# #             row_dict = dict(zip(columns, row))

# #             # Handle first check-in image
# #             if row_dict.get("first_check_in_image"):
# #                 filename = os.path.basename(row_dict["first_check_in_image"])
# #                 row_dict["first_check_in_image"] = request.build_absolute_uri(
# #                     f"/media/entry/{filename}"
# #                 )

# #             # Handle last check-out image
# #             if row_dict.get("last_check_out_image"):
# #                 filename = os.path.basename(row_dict["last_check_out_image"])
# #                 row_dict["last_check_out_image"] = request.build_absolute_uri(
# #                     f"/media/exit/{filename}"
# #                 )

# #             data.append(row_dict)

# #         return Response({"status": "success", "data": data})

# #     except Exception as e:
# #         return Response({"status": "error", "message": str(e)})

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db import connection
# import json
# import os
# from datetime import datetime

# from attendance_app.filters import build_common_filters


# # ✅ SAFE TIME PARSER
# def parse_time_safe(time_str):
#     try:
#         if not time_str:
#             return None

#         if '.' in time_str:
#             main, frac = time_str.split('.')
#             frac = (frac + "000000")[:6]
#             time_str = f"{main}.{frac}"

#         return datetime.fromisoformat(time_str)

#     except:
#         return None


# def get_clean_first_last(check_ins, check_outs):
#     ins = []
#     outs = []
#     events = []

#     # build IN
#     for x in check_ins:
#         t = parse_time_safe(x.get("time"))
#         if t:
#             ins.append((t, x.get("image")))
#             events.append((t, "IN", x.get("image")))

#     # build OUT
#     for x in check_outs:
#         t = parse_time_safe(x.get("time"))
#         if t:
#             outs.append((t, x.get("image")))
#             events.append((t, "OUT", x.get("image")))

#     # sort all
#     ins.sort(key=lambda x: x[0])
#     outs.sort(key=lambda x: x[0])
#     events.sort(key=lambda x: x[0])

#     first_in = ins[0] if ins else None
#     last_out = outs[-1] if outs else None

#     # 🔥 IMPORTANT CHECK
#     last_event = events[-1] if events else None

#     if last_event and last_event[1] == "IN":
#         # person came back again → no checkout
#         last_out = None

#     return first_in, last_out


# # ✅ IMAGE URL
# def build_url(request, path, type_):
#     if not path:
#         return None
#     filename = os.path.basename(path)
#     return request.build_absolute_uri(f"/media/{'entry' if type_=='IN' else 'exit'}/{filename}")


# @api_view(['GET'])
# def logs(request):
#     try:
#         date = request.GET.get('date')
#         range_type = request.GET.get('range')

#         # ✅ FIXED HERE
#         where_sql, params, _, _ = build_common_filters(date, range_type)

#         query = f"""
#             SELECT 
#                 ag.id,
#                 ag.per_id,
#                 ag.person_name,
#                 ag.attendance_date,
#                 ag.total_check_ins,
#                 ag.total_check_outs,
#                 ag.attendance_status,
#                 ag.all_check_in_images,
#                 ag.all_check_out_images,
#                 ps.shift_name

#             FROM attendance_aggre ag
#             LEFT JOIN person_shift ps 
#                 ON ag.per_id = ps.per_id

#             WHERE ag.person_name != 'Unknown'
#               AND {where_sql}

#             ORDER BY ag.attendance_date DESC
#         """

#         with connection.cursor() as cursor:
#             cursor.execute(query, params)
#             columns = [col[0] for col in cursor.description]
#             rows = cursor.fetchall()

#         final_data = []

#         for row in rows:
#             data = dict(zip(columns, row))

#             try:
#                 check_ins = json.loads(data.get("all_check_in_images") or "[]")
#                 check_outs = json.loads(data.get("all_check_out_images") or "[]")
#             except:
#                 check_ins, check_outs = [], []

#             first_in, last_out = get_clean_first_last(check_ins, check_outs)

#             first_check_in = first_in[0].isoformat() if first_in else None
#             first_img = build_url(request, first_in[1], "IN") if first_in else None

#             last_check_out = last_out[0].isoformat() if last_out else None
#             last_img = build_url(request, last_out[1], "OUT") if last_out else None

#             final_data.append({
#                 "id": data["id"],
#                 "per_id": data["per_id"],
#                 "person_name": data["person_name"],
#                 "attendance_date": data["attendance_date"],

#                 "first_check_in": first_check_in,
#                 "first_check_in_image": first_img,

#                 "last_check_out": last_check_out,
#                 "last_check_out_image": last_img,

#                 "total_check_ins": data["total_check_ins"],
#                 "total_check_outs": data["total_check_outs"],
#                 "attendance_status": data["attendance_status"],
#                 "shift_name": data["shift_name"],
#             })

#         return Response({"status": "success", "data": final_data})

#     except Exception as e:
#         return Response({"status": "error", "message": str(e)})


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db import connection
# import json
# import os
# from datetime import datetime

# from attendance_app.filters import build_common_filters


# # ✅ SAFE TIME PARSER
# def parse_time_safe(time_str):
#     try:
#         if not time_str:
#             return None

#         if '.' in time_str:
#             main, frac = time_str.split('.')
#             frac = (frac + "000000")[:6]
#             time_str = f"{main}.{frac}"

#         return datetime.fromisoformat(time_str)

#     except:
#         return None


# # ✅ CLEAN FIRST IN / LAST OUT
# def get_clean_first_last(check_ins, check_outs):
#     ins = []
#     outs = []
#     events = []

#     # build IN
#     for x in check_ins:
#         t = parse_time_safe(x.get("time"))
#         if t:
#             ins.append((t, x.get("image")))
#             events.append((t, "IN", x.get("image")))

#     # build OUT
#     for x in check_outs:
#         t = parse_time_safe(x.get("time"))
#         if t:
#             outs.append((t, x.get("image")))
#             events.append((t, "OUT", x.get("image")))

#     # sort all
#     ins.sort(key=lambda x: x[0])
#     outs.sort(key=lambda x: x[0])
#     events.sort(key=lambda x: x[0])

#     first_in = ins[0] if ins else None
#     last_out = outs[-1] if outs else None

#     # 🔥 IMPORTANT CHECK
#     last_event = events[-1] if events else None

#     if last_event and last_event[1] == "IN":
#         last_out = None

#     return first_in, last_out


# # ✅ IMAGE URL BUILDER
# def build_url(request, path, type_):
#     if not path:
#         return None
#     filename = os.path.basename(path)
#     return request.build_absolute_uri(
#         f"/media/{'entry' if type_=='IN' else 'exit'}/{filename}"
#     )


# # ✅ MAIN LOGS API
# @api_view(['GET'])
# def logs(request):
#     try:
#         date = request.GET.get('date')
#         from_time = request.GET.get('from_time')
#         to_time = request.GET.get('to_time')

#         # ✅ FILTER BUILDER (UPDATED)
#         where_sql, params, _, _ = build_common_filters(
#             date=date,
#             from_time=from_time,
#             to_time=to_time
#         )

#         query = f"""
#             SELECT 
#                 ag.id,
#                 ag.per_id,
#                 ag.person_name,
#                 ag.attendance_date,
#                 ag.total_check_ins,
#                 ag.total_check_outs,
#                 ag.attendance_status,
#                 ag.all_check_in_images,
#                 ag.all_check_out_images,
#                 ps.shift_name

#             FROM attendance_aggre ag
#             LEFT JOIN person_shift ps 
#                 ON ag.per_id = ps.per_id

#             WHERE ag.person_name != 'Unknown'
#               AND {where_sql}

#             ORDER BY ag.attendance_date DESC
#         """

#         with connection.cursor() as cursor:
#             cursor.execute(query, params)
#             columns = [col[0] for col in cursor.description]
#             rows = cursor.fetchall()

#         final_data = []

#         for row in rows:
#             data = dict(zip(columns, row))

#             # ✅ SAFE JSON PARSE
#             try:
#                 check_ins = json.loads(data.get("all_check_in_images") or "[]")
#                 check_outs = json.loads(data.get("all_check_out_images") or "[]")
#             except:
#                 check_ins, check_outs = [], []

#             # ✅ CLEAN LOGIC
#             first_in, last_out = get_clean_first_last(check_ins, check_outs)

#             first_check_in = first_in[0].isoformat() if first_in else None
#             first_img = build_url(request, first_in[1], "IN") if first_in else None

#             last_check_out = last_out[0].isoformat() if last_out else None
#             last_img = build_url(request, last_out[1], "OUT") if last_out else None

#             final_data.append({
#                 "id": data["id"],
#                 "per_id": data["per_id"],
#                 "person_name": data["person_name"],
#                 "attendance_date": data["attendance_date"],

#                 "first_check_in": first_check_in,
#                 "first_check_in_image": first_img,

#                 "last_check_out": last_check_out,
#                 "last_check_out_image": last_img,

#                 "total_check_ins": data["total_check_ins"],
#                 "total_check_outs": data["total_check_outs"],
#                 "attendance_status": data["attendance_status"],
#                 "shift_name": data["shift_name"],
#             })

#         return Response({
#             "status": "success",
#             "data": final_data
#         })

#     except Exception as e:
#         return Response({
#             "status": "error",
#             "message": str(e)
#         })


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
import json
import os
from datetime import datetime


# ✅ SAFE TIME PARSER
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


# ✅ CLEAN FIRST IN / LAST OUT
def get_clean_first_last(check_ins, check_outs):
    ins = []
    outs = []
    events = []

    # build IN events
    for x in check_ins:
        t = parse_time_safe(x.get("time"))
        if t:
            ins.append((t, x.get("image")))
            events.append((t, "IN", x.get("image")))

    # build OUT events
    for x in check_outs:
        t = parse_time_safe(x.get("time"))
        if t:
            outs.append((t, x.get("image")))
            events.append((t, "OUT", x.get("image")))

    # sort all
    ins.sort(key=lambda x: x[0])
    outs.sort(key=lambda x: x[0])
    events.sort(key=lambda x: x[0])

    first_in = ins[0] if ins else None
    last_out = outs[-1] if outs else None

    # 🔥 If last event is IN → no checkout yet
    last_event = events[-1] if events else None
    if last_event and last_event[1] == "IN":
        last_out = None

    return first_in, last_out


from django.conf import settings

def build_url(request, path, type_):
    if not path:
        return None

    filename = os.path.basename(path)

    return f"{settings.MEDIA_URL}{'entry' if type_=='IN' else 'exit'}/{filename}"

# ✅ MAIN LOGS API (NO FILTERS)
@api_view(['GET'])
def logs(request):
    try:
        query = """
            SELECT 
                ag.id,
                ag.per_id,
                ag.person_name,
                ag.first_check_in,
                ag.attendance_date,
                ag.total_check_ins,
                ag.total_check_outs,
                ag.attendance_status,
                ag.all_check_in_images,
                ag.all_check_out_images,
                ps.shift_name

            FROM attendance_aggre ag
            LEFT JOIN person_shift ps 
                ON ag.per_id = ps.per_id

            WHERE ag.person_name NOT IN ('Unknown', 'Naveen')

            ORDER BY ag.attendance_date, ag.first_check_in DESC
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        final_data = []

        for row in rows:
            data = dict(zip(columns, row))

            # ✅ SAFE JSON PARSE
            try:
                check_ins = json.loads(data.get("all_check_in_images") or "[]")
                check_outs = json.loads(data.get("all_check_out_images") or "[]")
            except:
                check_ins, check_outs = [], []

            # ✅ GET FIRST IN / LAST OUT
            first_in, last_out = get_clean_first_last(check_ins, check_outs)

            first_check_in = first_in[0].isoformat() if first_in else None
            first_img = build_url(request, first_in[1], "IN") if first_in else None

            last_check_out = last_out[0].isoformat() if last_out else None
            last_img = build_url(request, last_out[1], "OUT") if last_out else None

            final_data.append({
                "id": data["id"],
                "per_id": data["per_id"],
                "person_name": data["person_name"],
                "attendance_date": data["attendance_date"],

                "first_check_in": first_check_in,
                "first_check_in_image": first_img,

                "last_check_out": last_check_out,
                "last_check_out_image": last_img,

                "total_check_ins": data["total_check_ins"],
                "total_check_outs": data["total_check_outs"],
                "attendance_status": data["attendance_status"],
                "shift_name": data["shift_name"],
            })

        return Response({
            "status": "success",
            "data": final_data
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        })
