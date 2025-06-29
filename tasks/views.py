from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
# OR relation use korar jnno eita import korte hobe
from django.db.models import Q

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
    """#retrive all data from tasks model"""
    # tasks=Task.objects.all()
    # return render(request,"show_task.html",{"tasks":tasks})



    """ #jekono akta kisur vitti te mane"PENDING" nam a jotogula project ase sb view kora"""
    # task=Task.objects.filter(status="PENDING")
    # return render(request,"show_task.html",{'tasks':task})

    """#show the task which due_date today"""
    # tasks=Task.objects.filter(due_date=date.today())
    # return render(request,"show_task.html",{'tasks':tasks})


    """Show the task whose priority is not Low"""
    # tasks=TaskDetail.objects.exclude(priority="L")
    # return render(request,"show_task.html",{'tasks':tasks})

    """show the task that contain 'paper' AND status=pending """
    # tasks=Task.objects.filter(title__icontains='c',status="PENDING")
    # return render(request,"show_task.html",{'tasks':tasks})


    """show the task which are status=Pending OR status=In_Progress"""
    # tasks=Task.objects.filter(Q(status="PENDING") | Q(status="IN_PROGRESS"))
    # return render(request,"show_task.html",{'tasks':tasks})
    

    """select_related (ForeignKey,OneToOne field) 2ta table join korar query"""
    # tasks=TaskDetail.objects.select_related('task').all() for One To One
    # for One to many or foreign key
    # tasks=Task.objects.select_related('project').all()   

    """prefetch_related (reverse foreign key,many to many)"""  
    # tasks=Project.objects.prefetch_related('task_set').all() 
    # for many to many
    # tasks=Task.objects.prefetch_related('assigned_to').all()   
    tasks=Employee.objects.prefetch_related('tasks').all()
    return render(request,"show_task.html",{'tasks':tasks})

   
