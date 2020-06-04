from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class Task(models.Model):
    filename = models.CharField(max_length=512)
    calc_nr = models.CharField(max_length=30)
    search_str = models.CharField(max_length=30)
    result = models.CharField(max_length=4096)
    done = models.BooleanField(default=False)
