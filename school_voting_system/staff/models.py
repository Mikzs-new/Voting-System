from django.db import models

# Create your models here.
class Staff(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    staff_id = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name