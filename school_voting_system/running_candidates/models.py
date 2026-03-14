from django.db import models

from current_semester_students.models import Student
from voting.models import Election

class Partylist(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.TextField(blank=True)

class Position(models.Model):
    title = models.CharField(max_length=255)
    seat_count = models.SmallIntegerField()

class Candidate(models.Model):
    student_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE
    )
    partylist = models.ForeignKey(
        Partylist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE
    )

    image_file = models.ImageField(
        upload_to="candidate_images/",
        blank=True,
        null=True
    )
    description = models.TextField(blank=True)
    link = models.TextField(blank=True)

