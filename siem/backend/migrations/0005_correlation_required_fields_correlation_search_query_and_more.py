# Generated by Django 4.0.6 on 2022-07-27 06:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_alert_options_alter_correlation_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='correlation',
            name='required_fields',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='correlation',
            name='search_query',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ucr',
            name='cron_next_run',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 27, 6, 43, 29, 768651, tzinfo=utc)),
        ),
    ]
