# Generated by Django 3.1.4 on 2021-10-22 18:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20211022_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 22, 18, 30, 18, 664924, tzinfo=utc)),
        ),
    ]
