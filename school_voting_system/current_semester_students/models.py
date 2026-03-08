from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    student_school_id = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    year_level = models.CharField(max_length=25)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
