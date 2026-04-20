# import os
# from datetime import date

# from django.conf import settings
# from django.http import JsonResponse
# from django.core.mail import EmailMultiAlternatives
# from django.db import connection


# def send_late_alert_mail(request):

#     today = date.today()
#     sent_count = 0

#     try:
#         # =========================
#         # FETCH DATA FROM DB
#         # =========================
#         with connection.cursor() as cursor:

#             cursor.execute("""
#                 SELECT id, person_name, delay_display,
#                        first_check_in_time, first_check_in_image
#                 FROM attendance_alerts
#                 WHERE alert_status = 'Late'
#                   AND alert_date = %s
#                   AND person_name <> 'Unknown'
#                   AND mail_sent_status = 'Pending'
#             """, [today])

#             rows = cursor.fetchall()

#         # =========================
#         # LOOP EACH RECORD
#         # =========================
#         for row in rows:

#             alert_id = row[0]
#             person_name = row[1]
#             delay_display = row[2]
#             checkin_time = row[3]
#             image_path = row[4]

#             # =========================
#             # HTML EMAIL TEMPLATE
#             # =========================
#             html_content = f"""
#             <!DOCTYPE html>
#             <html>
#             <body style="font-family:Arial;background:#f6f8fa;padding:20px;">
#                 <div style="max-width:600px;margin:auto;background:#fff;padding:20px;border-radius:10px;">
                    
#                     <h2>Employee Late Alert</h2>

#                     <p><b>Name:</b> {person_name}</p>
#                     <p><b>Delay:</b> {delay_display}</p>
#                     <p><b>Check-in:</b> {checkin_time.strftime("%I:%M %p") if checkin_time else ""}</p>

#                 </div>
#             </body>
#             </html>
#             """

#             # =========================
#             # CREATE EMAIL
#             # =========================
#             email = EmailMultiAlternatives(
#                 subject=f"Late Alert - {person_name}",
#                 body="Late alert notification",
#                 from_email=settings.EMAIL_HOST_USER,
#                 to=["mahesh.raja@prowesstics.com"]   # 🔴 change if needed
#             )

#             email.attach_alternative(html_content, "text/html")

#             # =========================
#             # ATTACH IMAGE
#             # =========================
#             if image_path and os.path.exists(image_path):
#                 with open(image_path, "rb") as f:
#                     email.attach(
#                         os.path.basename(image_path),
#                         f.read(),
#                         "image/jpeg"
#                     )

#             # =========================
#             # SEND EMAIL
#             # =========================
#             email.send()

#             # =========================
#             # UPDATE DB AFTER SUCCESS
#             # =========================
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     UPDATE attendance_alerts
#                     SET mail_sent_status = 'Sent',
#                         mail_sent_at = NOW(),
#                         mail_retry_count = COALESCE(mail_retry_count, 0)
#                     WHERE id = %s
#                 """, [alert_id])

#             sent_count += 1

#         return JsonResponse({
#             "status": "success",
#             "sent_count": sent_count
#         })

#     except Exception as e:

#         # =========================
#         # OPTIONAL: RETRY COUNT UPDATE (GLOBAL FAIL SAFE)
#         # =========================
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 UPDATE attendance_alerts
#                 SET mail_retry_count = COALESCE(mail_retry_count, 0) + 1
#                 WHERE mail_sent_status = 'Pending'
#             """)

#         return JsonResponse({
#             "status": "failed",
#             "error": str(e)
#         })

# import os
# from datetime import date

# from django.conf import settings
# from django.http import JsonResponse
# from django.core.mail import EmailMultiAlternatives
# from django.db import connection
# from email.mime.image import MIMEImage


# def send_late_alert_mail(request):

#     today = date.today()
#     sent_count = 0

#     try:
#         with connection.cursor() as cursor:

#             cursor.execute("""
#                 SELECT id, person_name, delay_display,
#                        first_check_in_time, first_check_in_image
#                 FROM attendance_alerts
#                 WHERE alert_status = 'Late'
#                   AND alert_date = %s
#                   AND person_name <> 'Unknown'
#                   AND mail_sent_status = 'Pending'
#             """, [today])

#             rows = cursor.fetchall()

#         for row in rows:

#             alert_id = row[0]
#             person_name = row[1]
#             delay_display = row[2]
#             checkin_time = row[3]
#             image_path = row[4]

#             formatted_time = checkin_time.strftime("%I:%M %p") if checkin_time else ""

#             image_cid = "checkin_image"

#             # =========================
#             # YOUR HTML (UNCHANGED)
#             # =========================
#             html_content = f"""
#             <!DOCTYPE html>
#             <html lang="en">
#             <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>Late Notification</title>

#             <style>
#             @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

#             body {{
#                 font-family: 'Outfit', sans-serif;
#                 background-color: #f6f8fa;
#                 margin: 0;
#                 padding: 40px 20px;
#             }}

#             .container {{
#                 max-width: 600px;
#                 margin: auto;
#             }}

#             .report-card {{
#                 background: #ffffff;
#                 border-radius: 24px;
#                 box-shadow: 0 20px 40px -10px rgba(0,0,0,0.05);
#                 position: relative;
#             }}

#             .status-indicator {{
#                 position: absolute;
#                 left: 0;
#                 top: 40px;
#                 bottom: 40px;
#                 width: 5px;
#                 background: #f6ad55;
#             }}

#             .report-header {{
#                 padding: 40px;
#             }}

#             .report-title {{
#                 font-size: 26px;
#                 font-weight: 700;
#             }}

#             .summary-box {{
#                 margin: 0 40px 30px;
#                 background: #f8fafc;
#                 padding: 20px;
#                 border-radius: 12px;
#                 display: grid;
#                 grid-template-columns: 1fr 1fr;
#                 gap: 15px;
#             }}

#             .item-label {{
#                 font-size: 11px;
#                 color: #718096;
#                 text-transform: uppercase;
#             }}

#             .item-value {{
#                 font-weight: 600;
#             }}

#             .vision-frame {{
#                 margin: 0 40px 30px;
#                 height: 150px;
#                 border: 1px dashed #ccc;
#                 display: flex;
#                 justify-content: center;
#                 align-items: center;
#                 overflow: hidden;
#             }}

#             .vision-frame img {{
#                 max-width: 100%;
#                 max-height: 100%;
#                 object-fit: contain;
#             }}

#             .report-footer {{
#                 padding: 30px 40px;
#                 text-align: center;
#             }}

#             .primary-action {{
#                 background: #2d3748;
#                 color: #fff;
#                 padding: 12px;
#                 display: block;
#                 border-radius: 10px;
#                 text-decoration: none;
#             }}
#             </style>
#             </head>

#             <body>

#             <div class="container">
#             <div class="report-card">

#             <div class="status-indicator"></div>

#             <div class="report-header">
#                 <h1 class="report-title">Employee Arrival: Beyond Threshold</h1>
#             </div>

#             <div class="summary-box">
#                 <div>
#                     <div class="item-label">Member</div>
#                     <div class="item-value">{person_name}</div>
#                 </div>

#                 <div>
#                     <div class="item-label">Delay</div>
#                     <div class="item-value" style="color:#dd6b20;">{delay_display}</div>
#                 </div>

#                 <div>
#                     <div class="item-label">Shift Start</div>
#                     <div class="item-value">09:00 AM</div>
#                 </div>

#                 <div>
#                     <div class="item-label">Verified At</div>
#                     <div class="item-value">{formatted_time}</div>
#                 </div>
#             </div>

#             <div class="vision-frame">
#                 <img src="cid:{image_cid}" alt="reference detected image"/>
#             </div>

#             <div class="report-footer">
#                 <a href="#" class="primary-action">Manage in Dashboard</a>
#             </div>

#             </div>
#             </div>

#             </body>
#             </html>
#             """

#             # =========================
#             # EMAIL SETUP
#             # =========================
#             email = EmailMultiAlternatives(
#                 subject=f"Late Alert - {person_name}",
#                 body="Late alert notification",
#                 from_email=settings.EMAIL_HOST_USER,
#                 to=["mahesh.raja@prowesstics.com"]
#             )

#             email.attach_alternative(html_content, "text/html")

#             # =========================
#             # INLINE IMAGE (FIXED PROPER WAY)
#             # =========================
#             if image_path and os.path.exists(image_path):
#                 with open(image_path, "rb") as img:
#                     mime_image = MIMEImage(img.read())
#                     mime_image.add_header("Content-ID", "<checkin_image>")
#                     mime_image.add_header(
#                         "Content-Disposition",
#                         "inline",
#                         filename=os.path.basename(image_path)
#                     )
#                     email.attach(mime_image)

#             # =========================
#             # SEND EMAIL
#             # =========================
#             email.send()

#             # =========================
#             # UPDATE DB
#             # =========================
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     UPDATE attendance_alerts
#                     SET mail_sent_status = 'Sent',
#                         mail_sent_at = NOW(),
#                         mail_retry_count = COALESCE(mail_retry_count, 0)
#                     WHERE id = %s
#                 """, [alert_id])

#             sent_count += 1

#         return JsonResponse({
#             "status": "success",
#             "sent_count": sent_count
#         })

#     except Exception as e:

#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 UPDATE attendance_alerts
#                 SET mail_retry_count = COALESCE(mail_retry_count, 0) + 1
#                 WHERE mail_sent_status = 'Pending'
#             """)

#         return JsonResponse({
#             "status": "failed",
#             "error": str(e)
#         })



import os
from datetime import date
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.db import connection
from email.mime.image import MIMEImage


def send_late_alert_mail(request):

    today = date.today()
    sent_count = 0

    # ==================================================
    # FORMAT DELAY MINUTES -> HOURS & MINUTES
    # ==================================================
    def format_delay(minutes):
        if minutes is None:
            return ""

        hours = minutes // 60
        mins = minutes % 60

        if hours > 0:
            hour_text = "hour" if hours == 1 else "hours"
            minute_text = "minute" if mins == 1 else "minutes"
            return f"{hours} {hour_text} {mins} {minute_text}"
        else:
            minute_text = "minute" if mins == 1 else "minutes"
            return f"{mins} {minute_text}"

    # ==================================================
    # BUILD IMAGE URL FUNCTION
    # ==================================================
    # def build_url(request, image_path):
    #     if not image_path:
    #         return None

    #     filename = os.path.basename(image_path)
    #     folder = os.path.basename(os.path.dirname(image_path))

    #     return request.build_absolute_uri(
    #         f"/media/{folder}//{filename}"
    #     )
    def build_url(request, image_path):
        if not image_path:
            return None

        # normalize Windows path
        image_path = image_path.replace("\\", "/")

        # get filename
        filename = os.path.basename(image_path)

        # ✅ ONLY ENTRY KNOWN (as per your requirement)
        return f"https://provisions.blob.core.windows.net/media/entry/known/{filename}"

    # def build_url(request, image_path):
    #     if not image_path:
    #         return None

    #     filename = os.path.basename(image_path)
    #     folder = os.path.basename(os.path.dirname(image_path))

    #     url = request.build_absolute_uri(f"/media/{folder}/{filename}")

    #     return url.replace("http://", "https://")

    try:
        # ==================================================
        # FETCH PENDING LATE ALERTS
        # ==================================================
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT per_id, person_name,
                       delay_minutes,
                       first_check_in_time,
                       first_check_in_image
                FROM attendance_alerts
                WHERE alert_status = 'Late'
                  AND alert_date = %s
                  AND person_name <> 'Unknown'
                  AND mail_sent_status = 'Pending'
            """, [today])

            rows = cursor.fetchall()

        # ==================================================
        # SEND EMAILS
        # ==================================================
        for row in rows:

            alert_id = row[0]
            person_name = row[1]
            delay_minutes = row[2]
            checkin_time = row[3]
            image_path = row[4]

            formatted_time = checkin_time.strftime("%I:%M %p") if checkin_time else ""
            formatted_delay = format_delay(delay_minutes)

            image_cid = "checkin_image"

            
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Late Notification</title>
</head>

<body style="margin:0; padding:40px 20px; background-color:#f6f8fa; font-family:Arial, sans-serif;">

<div style="max-width:600px; margin:auto; background:#ffffff; border-radius:24px; box-shadow:0 20px 40px -10px rgba(0,0,0,0.05); position:relative;">

    <!-- Left indicator -->
    <div style="position:absolute; left:0; top:40px; bottom:40px; width:5px; background:#f6ad55;"></div>

    <!-- Header -->
    <div style="padding:40px;">
        <h1 style="font-size:26px; margin:0;">Employee Arrival: Beyond Threshold</h1>
    </div>

    <!-- Summary -->
    <div style="margin:0 40px 30px; background:#f8fafc; padding:20px; border-radius:12px;">
        
        <table width="100%" cellpadding="5" cellspacing="0">
            <tr>
                <td>
                    <div style="font-size:11px; color:#718096;">MEMBER</div>
                    <div style="font-weight:600;">{person_name}</div>
                </td>
                <td>
                    <div style="font-size:11px; color:#718096;">DELAY</div>
                    <div style="font-weight:600; color:#dd6b20;">+ {formatted_delay} Late</div>
                </td>
            </tr>
            <tr>
                <td>
                    <div style="font-size:11px; color:#718096;">SHIFT START</div>
                    <div style="font-weight:600;">10:30 AM</div>
                </td>
                <td>
                    <div style="font-size:11px; color:#718096;">VERIFIED AT</div>
                    <div style="font-weight:600;">{formatted_time}</div>
                </td>
            </tr>
        </table>

    </div>

    <!-- IMAGE FIXED SECTION -->
    <div style="margin:0 40px 30px;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" 
               style="border:1px dashed #ccc; border-radius:12px;">
            <tr>
                <td align="center" style="padding:10px; background:#f9f9f9;">
                    <img src="cid:{image_cid}" 
                         alt="Detected Image"
                         style="width:100%; max-width:100%; height:auto; display:block; border-radius:10px;">
                </td>
            </tr>
        </table>
    </div>

    <!-- Footer -->
    <div style="padding:30px 40px; text-align:center;">
        <a href="#" 
           style="background:#2d3748; color:#fff; padding:12px; display:block; border-radius:10px; text-decoration:none;">
           Manage in Dashboard
        </a>
    </div>

</div>

</body>
</html>
            """

            email = EmailMultiAlternatives(
                subject=f"Late Alert - {person_name}",
                body="Late alert notification",
                from_email=settings.EMAIL_HOST_USER,
                to=["mahesh.raja@prowesstics.com"]
            )

            email.attach_alternative(html_content, "text/html")

            # ============================
            # ATTACH IMAGE INLINE
            # ============================
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as img:
                    mime_image = MIMEImage(img.read())
                    mime_image.add_header("Content-ID", "<checkin_image>")
                    mime_image.add_header(
                        "Content-Disposition",
                        "inline",
                        filename=os.path.basename(image_path)
                    )
                    email.attach(mime_image)

            email.send()

            # ============================
            # UPDATE STATUS
            # ============================
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE attendance_alerts
                    SET mail_sent_status = 'Sent',
                        mail_sent_at = NOW(),
                        mail_retry_count = COALESCE(mail_retry_count, 0)
                    WHERE per_id = %s
                """, [alert_id])

            sent_count += 1

        # ==================================================
        # RETURN ALL LATE DATA
        # ==================================================
        with connection.cursor() as cursor:
            cursor.execute("""
                 SELECT per_id,
           person_name,
           alert_date,
           first_check_in_time,
           first_check_in_image,
           delay_minutes,
           mail_sent_status
    FROM attendance_alerts
    WHERE alert_status = 'Late'
      AND person_name <> 'Unknown'
    ORDER BY first_check_in_time DESC
            """)

            all_rows = cursor.fetchall()

        data = []

        for row in all_rows:
            data.append({
                "person_id": row[0],
                "person_name": row[1],
                "alert_date": str(row[2]),
                "first_checkin_time": row[3].strftime("%I:%M %p") if row[3] else None,
                "first_checkin_image": build_url(request, row[4]),
                "delay_display": format_delay(row[5]),
                "mail_status": row[6]
            })

        return JsonResponse({
            "status": "success",
            "sent_count": sent_count,
            "late_count": len(data),
            "data": data
        })

    except Exception as e:

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE attendance_alerts
                SET mail_retry_count = COALESCE(mail_retry_count, 0) + 1
                WHERE mail_sent_status = 'Pending'
            """)

        return JsonResponse({
            "status": "failed",
            "error": str(e)
        })


