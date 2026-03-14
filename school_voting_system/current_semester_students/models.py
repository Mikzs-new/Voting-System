from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)

class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    student_school_id = models.CharField(max_length=255)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    year_level = models.CharField(max_length=25)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
