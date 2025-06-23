from django.urls import path
from .views import manager_dashboard,user_dashboard,test

urlpatterns=[
    path('manager-dashboard/',manager_dashboard),
    path('user-dashboard/',user_dashboard),
    path('test/',test)
]