from django.db import models

from voting.models import SchoolYearElection

class VotingHistory(models.Model):
    school_election = models.ForeignKey(
        SchoolYearElection,
        on_delete=models.CASCADE
    )
    academic_year = models.CharField(max_length=255)