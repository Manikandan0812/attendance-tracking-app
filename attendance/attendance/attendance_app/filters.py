# from datetime import datetime, timedelta


# def build_common_filters(date=None, range_type=None):
#     where_conditions = []
#     params = []

#     now = datetime.now()

#     # ✅ DATE FILTER
#     if date:
#         where_conditions.append("DATE(attendance_date) = %s")
#         params.append(date)

#     # ✅ TIME RANGE FILTER (FIXED PROPERLY)
#     if range_type:
#         range_type = range_type.strip().lower()

#         if range_type in ["last 30 minutes", "last 30 mins"]:
#             start_time = now - timedelta(minutes=30)

#         elif range_type in ["last 1 hour", "last 1 hr"]:
#             start_time = now - timedelta(hours=1)

#         elif range_type in ["last 3 hours", "last 3 hrs"]:
#             start_time = now - timedelta(hours=3)

#         elif range_type == "" or range_type == "today":
#             start_time = datetime.combine(now.date(), datetime.min.time())

#         else:
#             start_time = None

#         if start_time:
#             # ✅ FIX: START + END (IMPORTANT)
#             where_conditions.append("""
#                 COALESCE(first_check_in, last_check_out)
#                 BETWEEN %s AND %s
#             """)
#             params.extend([start_time, now])

#     where_sql = " AND ".join(where_conditions) if where_conditions else "1=1"

#     return where_sql, params

# from datetime import datetime, timedelta

# def build_common_filters(date=None, range_type=None):
#     where_conditions = []
#     params = []

#     now = datetime.now()
#     start_time = None

#     # ✅ DATE FILTER
#     if date:
#         where_conditions.append("DATE(attendance_date) = %s")
#         params.append(date)

#     # ✅ RANGE FILTER
#     if range_type:
#         r = range_type.strip().lower()

#         if r in ["last 30 minutes", "last 30 mins"]:
#             start_time = now - timedelta(minutes=30)

#         elif r in ["last 1 hour", "last 1 hr"]:
#             start_time = now - timedelta(hours=1)

#         elif r in ["last 3 hours", "last 3 hrs"]:
#             start_time = now - timedelta(hours=3)

#         elif r == "today":
#             start_time = datetime.combine(now.date(), datetime.min.time())

#     # ✅ APPLY RANGE
#     if start_time:
#         where_conditions.append("""
#             (
#                 first_check_in BETWEEN %s AND %s
#                 OR last_check_out BETWEEN %s AND %s
#             )
#         """)
#         params.extend([start_time, now, start_time, now])

#     where_sql = " AND ".join(where_conditions) if where_conditions else "1=1"

#     # ✅ ALWAYS RETURN 4 VALUES
#     return where_sql, params, start_time, now


from datetime import datetime

def build_common_filters(date=None, range_type=None, from_time=None, to_time=None):
    where_conditions = []
    params = []

    start_time = None
    end_time = None

    # ✅ DATE FILTER (UNCHANGED)
    if date:
        where_conditions.append("DATE(attendance_date) = %s")
        params.append(date)

    # ✅ NEW TIME FILTER (FRONTEND DRIVEN)
    if from_time and to_time:
        try:
            start_time = datetime.fromisoformat(from_time)
            end_time = datetime.fromisoformat(to_time)

            where_conditions.append("""
                (
                    first_check_in BETWEEN %s AND %s
                    OR last_check_out BETWEEN %s AND %s
                )
            """)
            params.extend([start_time, end_time, start_time, end_time])

        except Exception:
            pass  # avoid breaking API if bad input

    where_sql = " AND ".join(where_conditions) if where_conditions else "1=1"

    return where_sql, params, start_time, end_time