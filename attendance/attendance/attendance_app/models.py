from django.db import models

class AttendanceEvent(models.Model):
    sno = models.AutoField(primary_key=True)
    per_id = models.IntegerField()
    person_name = models.CharField(max_length=100)

    entry_time = models.DateTimeField(null=True)
    exit_time = models.DateTimeField(null=True)

    evidence_image_entry = models.TextField(null=True)
    evidence_image_exit = models.TextField(null=True)

    created_at = models.DateTimeField()
    zone = models.CharField(max_length=50)

    class Meta:
        db_table = "attendance"   
        managed = False  