# Generated by Django 4.0.6 on 2022-08-01 07:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_alter_ucr_cron_next_run_alter_ucr_cron_previous_run'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ucr',
            name='cron_next_run',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 1, 7, 13, 47, 225429, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ucr',
            name='cron_previous_run',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 1, 7, 13, 47, 225457, tzinfo=utc), editable=False),
        ),
    ]