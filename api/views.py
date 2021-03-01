from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
# Create your views here.


class employeeList(APIView):

    def get(self, request):
        employe = employee.objects.all()        
        if request.method == "GET":
            if "id" in request.GET:
                id = request.GET.get("id")
                employe = employee.objects.filter(id = id)

        serializer = employeeSerializer(employe, many = True)
        return Response(serializer.data)

    def post(self):
        pass