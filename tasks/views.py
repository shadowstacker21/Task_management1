from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.contrib import messages
# OR relation use korar jnno eita import korte hobe
from django.db.models import Q,Count

# Create your views here.

def manager_dashboard(request):
   
   

    #getting task count
    # total_task=tasks.count()
    # completed_task=Task.objects.filter(status="COMPLETED").count()
    # in_progress_task=Task.objects.filter(status="IN_PROGRESS").count()
    # pending_task=Task.objects.filter(status="PENDING").count()
    type=request.GET.get('type','all')

   
    counts=Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id',filter=Q(status="COMPLETED")),
        in_progress=Count('id',filter=Q(status="IN_PROGRESS")),
        pending=Count('id',filter=Q(status="PENDING")),
        )
    
    
    #Retriving task data
    base_query=Task.objects.select_related('details').prefetch_related('assigned_to')

    if type=='completed':
        tasks=base_query.filter(status='COMPLETED')

    elif type=='in-progress':
        tasks=base_query.filter(status='IN_PROGRESS')

    if type=='pending':
        tasks=base_query.filter(status='PENDING')
    elif type=='all':
        tasks=base_query.all()    

    
    context={
        "tasks":tasks,
        "counts":counts
    }
    return render(request,"dashboard/manager-dashboard.html",context)

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
    task_form=TaskModelForm()
    task_detail_form=TaskDetailModelForm()
    if request.method == "POST":
        task_form=TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request,"Task Created Successfully")

            return redirect('create-task') 

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
             


    context={"task_form": task_form,"task_detail_form":task_detail_form}
    return render(request,"task_form.html",context)

def update_task(request,id):
    task=Task.objects.get(id=id)
    # employees=Employee.objects.all()
    task_form=TaskModelForm(instance=task)
    if task.details:
        task_detail_form=TaskDetailModelForm(instance=task.details)
    if request.method == "POST":
        task_form=TaskModelForm(request.POST,instance=task)
        task_detail_form=TaskDetailModelForm(request.POST,instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request,"Task updated Successfully")

            return redirect('update-task',id)

    context={"task_form": task_form,"task_detail_form":task_detail_form}
    return render(request,"task_form.html",context)

def delete_task(request,id):
    if request.method == 'POST':
        task=Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task Delete Successfully")
        return redirect('manager-dashboard')
    else:
        messages.error(request,"Something went wrong")
        return redirect('manager-dashboard')
        

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

   
