# Generated by Django 3.1.2 on 2021-03-01 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_remove_lunchattendance_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='lunchattendance',
            name='my_d',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='lunchattendance',
            name='my_t',
            field=models.TimeField(null=True),
        ),
    ]
