from django.db import models

class Group(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256, default="New group", null=True, blank=True)
    index = models.CharField(max_length=64)
    sourcetype = models.CharField(max_length=64)

class UCR(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256, default="New use case rule", null=True, blank=True)
    author = models.CharField(max_length=256, default="AYSOME IT Security", null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    cron = models.CharField(max_length=256, default="30 * * * *")
    search_terms = models.CharField(max_length=256, null=True, blank=True)
    search_query = models.TextField()

class Enrichment(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256, default="New enrichment", null=True, blank=True)
    author = models.CharField(max_length=256, default="AYSOME IT Security", null=True, blank=True)
    required_fields = models.CharField(max_length=256)
    required_groups = models.ManyToManyField(Group)
    search_query = models.TextField()


class Correlation(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256, default="New correlation", null=True, blank=True)
    author = models.CharField(max_length=256, default="AYSOME IT Security", null=True, blank=True)


class Alert(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256, default="New alert", null=True, blank=True)
    raw_event = models.TextField()
