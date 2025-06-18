from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    # Work with database
    # Transform data
    # Data pass
    # HTTP response or Json response
    return HttpResponse ("Welcome to the task management project")


def contact(request):
    return HttpResponse("This is contact page")

def show_task(request):
    return HttpResponse("This is show path")