from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task

# Create your views here.

def manager_dashboard(request):
    return render(request,"dashboard/manager-dashboard.html")

def user_dashboard(request):
    return render(request,"dashboard/user_dashboard.html")

def test(request):
    context={
        "names":["Alamin","Amirul","Jahidul","Programmer"],
        "age":20,
    }
    return render(request,"test.html",context)

def create_task(request):
    # employees=Employee.objects.all()
    form=TaskModelForm()
    if request.method == "POST":
        form=TaskModelForm(request.POST)
        if form.is_valid():

            """ For Model Form Data """
            form.save()

            return render(request,'task_form.html',{'form': form,"message":"Task Added Successfully"})

            """ For Django Form Data """
            # data=form.cleaned_data
            # title=data.get('title')
            # description=data.get('description')
            # due_date=data.get('due_date')
            # assigned_to=data.get('assigned_to')

            # task=Task.objects.create(title=title,description=description,due_date=due_date)
            

            # #Assign employee to task
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)

            # return HttpResponse ("Task Added Succesfully")  
             


    context={"form": form}
    return render(request,"task_form.html",context)

def view_task(request):
    #retrive all data from tasks model
    tasks=Task.objects.all()
    return render(request,"show_task.html",{"tasks":tasks})