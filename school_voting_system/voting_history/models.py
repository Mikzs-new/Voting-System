from django.db import models

from voting.models import SchoolElection

class VotingHistory(models.Model):
    school_election = models.ForeignKey(
        SchoolElection,
        on_delete=models.CASCADE
    )
    academic_year = models.CharField(max_length=255)