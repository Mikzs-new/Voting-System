from django.db import models

class Facilitator(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    facilitator_school_id = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name