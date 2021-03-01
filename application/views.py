from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json
from random import randint
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


class attendanceList(APIView):
    def time_in_range(self, start, end, x):
        """Return true if x is in the range [start, end]"""
        if end == x:
            return False

        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def checking_time_slot(self, timings, entered_time, entered_day):
        entered_day_schedule = timings[entered_day]
        if self.time_in_range(entered_day_schedule['start'], entered_day_schedule['end'], entered_time):
            print(entered_day, entered_day_schedule, entered_time)
            return entered_day_schedule
        else:
            return False

    def get(self, request):
        attendances = lunchAttendance.objects.all()        
        if request.method == "GET":
            if "id" in request.GET:
                id = request.GET.get("id")
                attendances = lunchAttendance.objects.filter(id = id)

        serializer = attendanceSerializer(attendances, many = True)
        return Response({})

    def post(self, request):
        if request.method == "POST":
            my_response = {
                'status': False, #or false in case of wrong qr code
                'user_data': {
                    'first_name': None,
                    'last_name': None
                },
                'is_allowed': False, #or false in case he is not allowed
                'message': None
            }

            try:
                if "code" in request.POST and "date" in request.POST and "time" in request.POST:
                    code = request.POST['code']
                    date = request.POST['date']
                    time = request.POST['time']
                    day = request.POST['day']

                    if Employee.objects.filter(unique_id = code).exists():
                        focused_employee = Employee.objects.get(unique_id = code)
                        focused_employee_data = focused_employee.get_details()
                        my_response['status'] = True
                        my_response['user_data']['first_name'] = focused_employee.first_name
                        my_response['user_data']['last_name'] = focused_employee.last_name
                        
                        splitted_date = date.split("-")
                        splitted_time = time.split(":")

                        timestamp = datetime(
                            year = int(splitted_date[-1]), 
                            month = int(splitted_date[1]), 
                            day = int(splitted_date[0]),
                            hour = int(splitted_time[0]),
                            minute = int(splitted_time[1]),
                            second = int(splitted_time[2])
                        )

                        if lunchAttendance.objects.filter(my_d = timestamp.date(), employee = focused_employee).exists():
                            my_response['is_allowed'] = False
                            my_response['message'] = "Not allowed! You already visited the canteen in this shift."
                        else:
                            our_entered_time_object = datetime.strptime(time, '%H:%M:%S').time()
                            is_in_range = self.checking_time_slot(focused_employee_data['timings'], our_entered_time_object, day)

                            if is_in_range:
                                my_response['is_allowed'] = True
                                my_response['message'] = "You are allowed to go into the canteen"

                                mark_attendance = lunchAttendance(
                                    employee =  focused_employee,
                                    shift_start_time = is_in_range['start'],
                                    shift_end_time = is_in_range['end'],
                                    my_d = timestamp.date(),
                                    my_t = timestamp.time()
                                )

                                mark_attendance.save()

                            else:
                                my_response['is_allowed'] = False
                                my_response['message'] = "You are not allowed to go into the canteen!"

                    else:
                        my_response['status'] = False
                        my_response['message'] = 'Something went wrong!'

                else:
                    my_response['status'] = False
                    my_response['message'] = "Something went wrong!"
            except:
                my_response['status'] = False
                my_response['message'] = "Something went wrong!"

            return Response(my_response)


# main page function
def getEmployee(request):
    output = {}
    try:
        if request.method == "GET" and request.is_ajax():
            employee_id = int(request.GET['employee_id'])
            
            if Employee.objects.filter(id = employee_id).exists():
                output['status'] = True
                employee_object =  Employee.objects.get(id = employee_id)
                output['employee_info'] = employee_object.get_details()
            else:
                output['status'] = False
    except:
        output['status'] = False
    
    return JsonResponse(output)



def employees(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("login")

    all_employees = Employee.objects.all()
    return render(request, "list-employees.html", {'all_employees': all_employees})


def addEmployee(request):
    if request.method == "POST":
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        monday_from = request.POST['monday-from']
        monday_to = request.POST['monday-to']
        tuesday_from = request.POST['tuesday-from']
        tuesday_to = request.POST['tuesday-to']
        wednesday_from = request.POST['wednesday-from']
        wednesday_to = request.POST['wednesday-to']
        thursday_from = request.POST['thursday-from']
        thursday_to = request.POST['thursday-to']
        friday_from = request.POST['friday-from']
        friday_to = request.POST['friday-to']
        saturday_from = request.POST['saturday-from']
        saturday_to = request.POST['saturday-to']
        sunday_from = request.POST['sunday-from']
        sunday_to = request.POST['sunday-to']

        new_employee = Employee(
            first_name = first_name,
            last_name = last_name,
            monday_start_time = monday_from,
            monday_end_time = monday_to,
            tuesday_start_time = tuesday_from,
            tuesday_end_time = tuesday_to,
            wednesday_start_time = wednesday_from,
            wednesday_end_time = wednesday_to,
            thursday_start_time = thursday_from,
            thursday_end_time = thursday_to,
            friday_start_time = friday_from,
            friday_end_time = friday_to,
            saturday_start_time = saturday_from,
            saturday_end_time = saturday_to,
            sunday_start_time = sunday_from,
            sunday_end_time = sunday_to,
        )

        new_employee.save()

        return redirect("index")

def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'main.html')


# function for signup

def signup(request):
    return redirect("login")

    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()
            
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)


    
    return render(request, "signup.html")


# function for login

def login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "login.html", context)
            # return redirect("login")
    else:
        return render(request, "login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")

