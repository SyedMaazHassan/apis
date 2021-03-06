# Generated by Django 3.1.2 on 2021-02-24 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('application', '0008_delete_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(editable=False, max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('monday_start_time', models.TimeField()),
                ('monday_end_time', models.TimeField()),
                ('tuesday_start_time', models.TimeField()),
                ('tuesday_end_time', models.TimeField()),
                ('wednesday_start_time', models.TimeField()),
                ('wednesday_end_time', models.TimeField()),
                ('thursday_start_time', models.TimeField()),
                ('thursday_end_time', models.TimeField()),
                ('friday_start_time', models.TimeField()),
                ('friday_end_time', models.TimeField()),
                ('saturday_start_time', models.TimeField()),
                ('saturday_end_time', models.TimeField()),
                ('sunday_start_time', models.TimeField()),
                ('sunday_end_time', models.TimeField()),
            ],
        ),
    ]
