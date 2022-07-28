# Generated by Django 4.0.6 on 2022-07-28 07:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_ucr_cron_next_run'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucr',
            name='cron_previous_run',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 28, 7, 58, 43, 347610, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ucr',
            name='cron_next_run',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 28, 7, 58, 43, 347585, tzinfo=utc)),
        ),
    ]
