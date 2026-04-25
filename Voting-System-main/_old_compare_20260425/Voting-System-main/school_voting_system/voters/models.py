from django.db import models

from running_candidates.models import Candidate, Position
from current_semester_students.models import Student
from voting.models import Election

class Vote(models.Model):
    student_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE
    )
    
    datetime = models.DateTimeField(auto_now_add=True)

class VoteItem(models.Model):
    voter = models.ForeignKey(
        Vote,
        on_delete=models.CASCADE
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )