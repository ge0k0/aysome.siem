from django.db import models

class UCR_Testing(models.Model):
    title = models.CharField(max_length=256, primary_key=True, unique=True)
    description = models.CharField(max_length=256, default="New use case rule", null=True, blank=True)
    author = models.CharField(max_length=256, default="AYSOME IT Security", null=True, blank=True)

    index = models.CharField(max_length=256, default="main")
    sourcetype = models.CharField(max_length=256, default="api")

    variables = models.CharField(max_length=256, null=True, blank=True)
    search_query = models.TextField()
    threshhold = models.IntegerField(default=1)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "UCR"
        verbose_name_plural = "UCRs"