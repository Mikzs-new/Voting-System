from django.db import models

from facilitators.models import Facilitator

class Election(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created_by = models.ForeignKey(
        Facilitator,
        on_delete=models.CASCADE,
        null=True
    )

    creation_date = models.DateField(auto_now_add=True)

    start_voting_date = models.DateTimeField()
    end_voting_date = models.DateTimeField()

class SchoolElection(models.Model):
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)

    academic_year = models.CharField(max_length=20)

    creation_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()