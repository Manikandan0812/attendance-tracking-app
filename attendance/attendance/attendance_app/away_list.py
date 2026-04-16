from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from datetime import datetime
import json
import os

from attendance_app.filters import build_common_filters


# ✅ SAFE TIME PARSER (handles microseconds)
def parse_time_safe(time_str):
    try:
        if not time_str:
            return None

        if '.' in time_str:
            main, frac = time_str.split('.')
            frac = (frac + "000000")[:6]
            time_str = f"{main}.{frac}"

        return datetime.fromisoformat(time_str)

    except Exception as e:
        print("Time parse error:", time_str, e)
        return None


# ✅ IMAGE URL BUILDER
def build_image_url(request, path, img_type):
    if not path:
        return None

    filename = os.path.basename(path)

    if img_type == "IN":
        return request.build_absolute_uri(f"/media/entry/{filename}")
    else:
        return request.build_absolute_uri(f"/media/exit/{filename}")

# def build_image_url(request, path, img_type):
#     if not path:
#         return None

#     filename = os.path.basename(path)

#     if img_type == "IN":
#         url = request.build_absolute_uri(f"/media/entry/{filename}")
#     else:
#         url = request.build_absolute_uri(f"/media/exit/{filename}")

#     # Force https (useful behind ngrok / proxy)
#     return url.replace("http://", "https://")


# ✅ FIXED AWAY CALCULATION (handles multiple pairs correctly)
def calculate_away(all_check_ins, all_check_outs, request):
    try:
        events = []

        # IN events
        for x in all_check_ins:
            t = parse_time_safe(x.get("time"))
            if t:
                events.append({
                    "time": t,
                    "type": "IN",
                    "image": x.get("image")
                })

        # OUT events
        for x in all_check_outs:
            t = parse_time_safe(x.get("time"))
            if t:
                events.append({
                    "time": t,
                    "type": "OUT",
                    "image": x.get("image")
                })

        # Sort all events
        events.sort(key=lambda x: x["time"])

        away_list = []
        total_away = 0
        last_out_event = None

        for event in events:

            if event["type"] == "OUT":
                last_out_event = event

            elif event["type"] == "IN" and last_out_event:
                diff = (event["time"] - last_out_event["time"]).total_seconds()

                if diff > 30:  # ignore noise
                    away_list.append({
                        "out_time": last_out_event["time"].strftime("%Y-%m-%d %H:%M:%S"),
                        "out_image": build_image_url(request, last_out_event["image"], "OUT"),

                        "in_time": event["time"].strftime("%Y-%m-%d %H:%M:%S"),
                        "in_image": build_image_url(request, event["image"], "IN"),

                        "away_seconds": int(diff)
                    })

                    total_away += diff

                # reset after pairing
                last_out_event = None

        return int(total_away), away_list

    except Exception as e:
        print("Away calc error:", e)
        return 0, []


# ✅ OPTIONAL: FULL TIMELINE (for debugging / UI)
def build_timeline(all_check_ins, all_check_outs, request):
    events = []

    for x in all_check_ins:
        t = parse_time_safe(x.get("time"))
        if t:
            events.append({
                "time": t,
                "type": "IN",
                "image": build_image_url(request, x.get("image"), "IN")
            })

    for x in all_check_outs:
        t = parse_time_safe(x.get("time"))
        if t:
            events.append({
                "time": t,
                "type": "OUT",
                "image": build_image_url(request, x.get("image"), "OUT")
            })

    events.sort(key=lambda x: x["time"])

    for e in events:
        e["time"] = e["time"].strftime("%Y-%m-%d %H:%M:%S")

    return events


# ✅ MAIN API
@api_view(['GET'])
def away_logs(request):
    try:
        date = request.GET.get('date')
        range_type = request.GET.get('range')

        # ✅ IMPORTANT FIX (NO unpack error)
        where_sql, params, _, _ = build_common_filters(date, range_type)

        query = f"""
        SELECT 
            ag.id,
            ag.per_id,
            ag.person_name,
            ag.attendance_date,
            ag.first_check_in,

            CASE 
                WHEN ag.last_check_out IS NULL THEN NULL
                WHEN ag.first_check_in > ag.last_check_out THEN NULL
                ELSE ag.last_check_out
            END AS last_check_out,

            CASE 
                WHEN ag.last_check_out IS NULL THEN NULL
                WHEN ag.first_check_in > ag.last_check_out THEN NULL
                ELSE ag.last_check_out_image
            END AS last_check_out_image,

            ag.total_check_ins,
            ag.total_check_outs,
            ag.total_in_out_pairs,
            ag.assigned_shift_id,
            ag.assigned_shift_name,
            ag.total_calculated_work_hours,

            ag.first_check_in_image,
            ag.all_check_in_images,
            ag.all_check_out_images

        FROM attendance_aggre ag
        WHERE ag.person_name != 'Unknown'
          AND {where_sql}

        ORDER BY ag.attendance_date DESC
        """

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        results = []

        for row in rows:
            data = dict(zip(columns, row))

            # ✅ Parse JSON safely
            try:
                check_ins = json.loads(data.get("all_check_in_images") or "[]")
                check_outs = json.loads(data.get("all_check_out_images") or "[]")
            except:
                check_ins, check_outs = [], []

            # ✅ AWAY CALCULATION
            away_time, away_list = calculate_away(check_ins, check_outs, request)

            # ✅ TIMELINE (optional)
            timeline = build_timeline(check_ins, check_outs, request)

            # ✅ IMAGE FIX
            first_img = build_image_url(request, data.get("first_check_in_image"), "IN")
            last_img = build_image_url(request, data.get("last_check_out_image"), "OUT")

            results.append({
                "id": data["id"],
                "per_id": data["per_id"],
                "person_name": data["person_name"],
                "attendance_date": data["attendance_date"],

                "away_time": away_time,
                "first_checkin-last_checkout_list": away_list,

                # 🔥 FULL DEBUG VISIBILITY
                "timeline": timeline,

                "first_check_in": data["first_check_in"],
                "first_check_in_image": first_img,

                "last_check_out": data["last_check_out"],
                "last_check_out_image": last_img,

                "total_check_ins": data["total_check_ins"],
                "total_check_outs": data["total_check_outs"],
                "total_in_out_pairs": data["total_in_out_pairs"],
                "assigned_shift_id": data["assigned_shift_id"],
                "assigned_shift_name": data["assigned_shift_name"],
                "total_calculated_work_hours": data["total_calculated_work_hours"],
            })

        return Response({
            "status": "success",
            "data": results
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)