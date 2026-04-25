from django.db import models

from facilitators.models import Facilitator
from current_semester_students.models import Course

class SchoolYearElection(models.Model):
    title = models.CharField(max_length=255)

    academic_year = models.CharField(max_length=20)

    creation_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title + ' ' + self.academic_year

class Election(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created_by = models.ForeignKey(
        Facilitator,
        on_delete=models.CASCADE,
        null=True
    )

    school_election = models.ForeignKey(
        SchoolYearElection,
        on_delete=models.CASCADE,
        null=True
    )

    available = models.BooleanField(default=True)
    creation_date = models.DateField(auto_now_add=True)

    start_voting_date = models.DateTimeField()
    end_voting_date = models.DateTimeField()

    def __str__(self):
        return self.title

class YearLevelValidItem(models.Model):
    year_level = models.SmallIntegerField()
    election_id = models.ForeignKey(
        Election,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return str(self.year_level) + ' - ' + self.election_id.__str__()
    

class CoursesValidItem(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    election_id = models.ForeignKey(
        Election,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.course.__str__() + ' - ' + self.election_id.__str__()