from django.db import models

class Election(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    creation_date = models.DateField(auto_now_add=True)

    start_voting_date = models.DateField()
    end_voting_date = models.DateField()

class SchoolElection(models.Model):
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)

    academic_year = models.CharField(max_length=20)

    creation_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()