from django.db import models

class itemPage(models.Model):
    name = models.CharField(max_length=4)

class champPage(models.Model):
    name = models.CharField(max_length=4)

class stat(models.Model):
    name = models.CharField(max_length=4)
    value = models.CharField(max_length=100)

class JSON(models.Model):
    entries = models.ManyToManyField("self", symmetrical=False)
    value = models.CharField(max_length=100)
    done = models.CharField(max_length=1)
