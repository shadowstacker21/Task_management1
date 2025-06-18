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

def show_specific_task(request,id):
    print("ID",id)
    print("Id Type",type(id))
    return HttpResponse (f"This is dynamic urls {id}")