from rest_framework import serializers
from .models import *
# from rest_framework import employee

class attendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = lunchAttendance
        # fields = ('first_name', 'last_name')
        fields = "__all__"