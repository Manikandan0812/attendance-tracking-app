from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from django.conf import settings
from datetime import datetime
import json
import os
import re


# ==============================
# SAFE TIME PARSER
# ==============================
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


# ==============================
# FIX WINDOWS ESCAPE ISSUE (ROOT FIX)
# ==============================
def normalize_path(path):
    """
    Fixes:
    D:\Vision Analytics\...
    \V, \F invalid escape warnings
    """
    if not path:
        return None

    # convert to raw-safe string first
    path = str(path)

    # FIX BACKSLASH ISSUE
    path = path.replace("\\", "/")

    # remove duplicate slashes
    path = re.sub(r"/+", "/", path)

    return path


# ==============================
# EXTRACT entry/exit CLEAN PATH
# ==============================
def clean_image_path(path):
    path = normalize_path(path)

    if not path:
        return None

    parts = path.split("/")

    if "entry" in parts:
        idx = parts.index("entry")
    elif "exit" in parts:
        idx = parts.index("exit")
    else:
        return os.path.basename(path)

    return "/".join(parts[idx:])


# ==============================
# BUILD FINAL IMAGE URL (AZURE)
# ==============================
def build_image_url(request, path, img_type):
    clean_path = clean_image_path(path)

    if not clean_path:
        return None

    return f"{settings.MEDIA_URL}{clean_path}"


# ==============================
# SAFE TIMELINE PARSER
# ==============================
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


# ==============================
# AWAY CALCULATION
# ==============================
def calculate_away(all_check_ins, all_check_outs, request):
    try:
        events = []

        for x in all_check_ins:
            t = parse_time_safe(x.get("time"))
            if t:
                events.append({"time": t, "type": "IN", "image": x.get("image")})

        for x in all_check_outs:
            t = parse_time_safe(x.get("time"))
            if t:
                events.append({"time": t, "type": "OUT", "image": x.get("image")})

        events.sort(key=lambda x: x["time"])

        away_list = []
        total_away = 0
        last_out = None

        for e in events:
            if e["type"] == "OUT":
                last_out = e

            elif e["type"] == "IN" and last_out:
                diff = (e["time"] - last_out["time"]).total_seconds()

                if diff > 30:
                    away_list.append({
                        "out_time": last_out["time"].strftime("%Y-%m-%d %H:%M:%S"),
                        "out_image": build_image_url(request, last_out["image"], "OUT"),

                        "in_time": e["time"].strftime("%Y-%m-%d %H:%M:%S"),
                        "in_image": build_image_url(request, e["image"], "IN"),

                        "away_seconds": int(diff)
                    })

                    total_away += diff

                last_out = None

        return int(total_away), away_list

    except:
        return 0, []


# ==============================
# MAIN API
# ==============================
@api_view(['GET'])
def away_logs(request):
    try:
        where_sql, params, _, _ = build_common_filters(
            request.GET.get('date'),
            request.GET.get('range')
        )

        query = f"""
        SELECT 
            ag.id,
            ag.per_id,
            ag.person_name,
            ag.attendance_date,
            ag.first_check_in,
            ag.last_check_out,
            ag.last_check_out_image,
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

            # SAFE JSON PARSE
            try:
                check_ins = json.loads(data.get("all_check_in_images") or "[]")
                check_outs = json.loads(data.get("all_check_out_images") or "[]")
            except:
                check_ins, check_outs = [], []

            away_time, away_list = calculate_away(check_ins, check_outs, request)
            timeline = build_timeline(check_ins, check_outs, request)

            results.append({
                "id": data["id"],
                "per_id": data["per_id"],
                "person_name": data["person_name"],
                "attendance_date": data["attendance_date"],

                "away_time": away_time,
                "first_checkin-last_checkout_list": away_list,
                "timeline": timeline,

                "first_check_in": data["first_check_in"],
                "first_check_in_image": build_image_url(request, data.get("first_check_in_image"), "IN"),
                "last_check_out": data["last_check_out"],
                "last_check_out_image": build_image_url(request, data.get("last_check_out_image"), "OUT"),

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
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)
