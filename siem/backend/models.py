from django.db import models
from django.utils import timezone

class Group(models.Model):
    title = models.CharField(max_length=256, primary_key=True, unique=True)
    description = models.CharField(max_length=256, default="New group", null=True, blank=True)
    author = models.CharField(max_length=256, default="AYSOME IT Security", null=True, blank=True)
    search_query_prefix = models.CharField(max_length=256, default='', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "group"
        verbose_name_plural = "groups"

class UCR(models.Model):
    title = models.CharField(max_length=256, primary_key=True, unique=True)
    description = models.CharField(max_length=256, default="New use case rule", null=True, blank=True)
    author = models.CharField(max_length=256, default="AYSOME IT Security", null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    cron = models.CharField(max_length=256, default="30 * * * *")
    cron_next_run = models.DateTimeField(default=timezone.now())
    cron_previous_run = models.DateTimeField(default=timezone.now(), editable=False)
    search_terms = models.CharField(max_length=256, null=True, blank=True)
    search_query = models.TextField()
    threshhold = models.IntegerField(default=1)
    threshhold_group_by_fields = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "UCR"
        verbose_name_plural = "UCRs"

class Enrichment(models.Model):
    title = models.CharField(max_length=256, primary_key=True, unique=True)
    description = models.CharField(max_length=256, default="New enrichment", null=True, blank=True)
    author = models.CharField(max_length=256, default="AYSOME IT Security", null=True, blank=True)
    group = models.ManyToManyField(Group)
    required_fields = models.CharField(max_length=256)
    search_query = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "enrichment"
        verbose_name_plural = "enrichments"

class Correlation(models.Model):
    title = models.CharField(max_length=256, primary_key=True, unique=True)
    description = models.CharField(max_length=256, default="New correlation", null=True, blank=True)
    author = models.CharField(max_length=256, default="AYSOME IT Security", null=True, blank=True)
    required_fields = models.CharField(max_length=256, null=True, blank=True)
    search_query = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "correlation"
        verbose_name_plural = "correlations"

class Alert(models.Model):
    title = models.CharField(max_length=256, primary_key=True, unique=True)
    description = models.CharField(max_length=256, default="New alert", null=True, blank=True)
    author = models.CharField(max_length=256, default="AYSOME IT Security", null=True, blank=True)
    raw_event = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "alert"
        verbose_name_plural = "alerts"