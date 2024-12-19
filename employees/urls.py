from django.urls import path
from rest_framework.permissions import AllowAny

from employees.apps import EmployeesConfig
from employees.views import MyTokenObtainPairView, MyTokenRefreshView

app_name = EmployeesConfig.name

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(
        permission_classes=[AllowAny]), name="token_obtain_pair"),
    path("token/refresh/", MyTokenRefreshView.as_view(
        permission_classes=[AllowAny]), name="token_refresh"),
]
