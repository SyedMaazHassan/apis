from django.urls import path
from . import views
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('addEmployee', views.addEmployee, name="addEmployee"),
    path('employees', views.employees, name="employees"),
    path('getEmployee', views.getEmployee, name="getEmployee"),
    path('api', views.attendanceList.as_view())
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
