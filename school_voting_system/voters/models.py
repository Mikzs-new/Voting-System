from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    year = models.SmallIntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=255)