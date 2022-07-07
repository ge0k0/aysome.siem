from signal import alarm
from django.contrib import admin
from backend.models import *

admin.site.register(Group)
admin.site.register(UCR)
admin.site.register(Enrichment)
admin.site.register(Correlation)
admin.site.register(Alert)