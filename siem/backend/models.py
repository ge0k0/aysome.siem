from django.db import models

class Group(models.Model):
    title = models.CharField(max_length=256)
    index = models.CharField(max_length=64)
    sourcetype = models.CharField(max_length=64)

class UCR(models.Model):
    title = models.CharField(max_length=256)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    search_query = models.TextField()

class Enrichment(models.Model):
    title = models.CharField(max_length=256)


class Correlation(models.Model):
    title = models.CharField(max_length=256)


class Alert(models.Model):
    title = models.CharField(max_length=256)
