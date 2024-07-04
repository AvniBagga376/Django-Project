from django.db import models
from datetime import date

## Create your models here.
#
class Contact(models.Model):
    name= models.CharField(max_length=122)
    phone= models.CharField(max_length=12)
    email = models.CharField(max_length=122)
    desc = models.TextField(max_length=200)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.name