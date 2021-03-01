from django.db import models
from datetime import datetime
from random import randint
from django.contrib.auth.models import User, auth
# Create your models here.

class Employee(models.Model):
    unique_id = models.CharField(max_length = 255, editable = False)
    
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)

    monday_start_time = models.TimeField()
    monday_end_time = models.TimeField()

    tuesday_start_time = models.TimeField()
    tuesday_end_time = models.TimeField()

    wednesday_start_time = models.TimeField()
    wednesday_end_time = models.TimeField()

    thursday_start_time = models.TimeField()
    thursday_end_time = models.TimeField()

    friday_start_time = models.TimeField()
    friday_end_time = models.TimeField()

    saturday_start_time = models.TimeField()
    saturday_end_time = models.TimeField()

    sunday_start_time = models.TimeField()
    sunday_end_time = models.TimeField()

    def random_code(self, length):
        '''
        This function will return a string of random 
        alphanumeric code of given length (integer)
        '''
        CHAR = "01234BCDEFGHIJ56789afghijklmnopqLMNOPQRSTUrstuvwxyzAKbcdeVWXYZ"
        code = ""
        for i in range(0, length):
            index = randint(0, len(CHAR)-1)
            code += CHAR[index]
        return code

    def get_details(self):
        return {
            "unique_id": self.unique_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "timings": {
                "Mon": {
                    "start": self.monday_start_time,
                    "end": self.monday_end_time,
                },
                "Tue": {
                    "start": self.tuesday_start_time,
                    "end": self.tuesday_end_time,
                },
                "Wed": {
                    "start": self.wednesday_start_time,
                    "end": self.wednesday_end_time,
                },
                "Thu": {
                    "start": self.thursday_start_time,
                    "end": self.thursday_end_time,
                },
                "Fri": {
                    "start": self.friday_start_time,
                    "end": self.friday_end_time,
                },
                "Sat": {
                    "start": self.saturday_start_time,
                    "end": self.saturday_end_time,
                },
                "Sun": {
                    "start": self.sunday_start_time,
                    "end": self.sunday_end_time,
                }
            }
        }
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.unique_id = self.random_code(50)
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} - {self.unique_id}' 


class lunchAttendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift_start_time = models.TimeField()
    shift_end_time = models.TimeField()
    my_d = models.DateField(null = True)
    my_t = models.TimeField(null = True)

    def __str__(self):
        return self.employee.first_name


# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


