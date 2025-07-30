from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Task,TaskDetail,Project
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required
# OR relation use korar jnno eita import korte hobe
from django.db.models import Q,Count
from users.views import is_admin
from django.http import HttpResponse
from django.views import View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView,DetailView,UpdateView,DeleteView


#class_Based_View Re use example

class Greetings(View):
    greetings = 'Hello Everyone'

    def get(self,request):
        return HttpResponse(self.greetings)

class HiGreetings(Greetings):
    greetings = 'Hi Everyone'
# Create your views here.

def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_employee(user):
    return user.groups.filter(name='Employee').exists()

@method_decorator(user_passes_test(is_manager, login_url='no-permission'), name='dispatch')
class ManagerView(ListView):
    model = Task
    template_name = "dashboard/manager-dashboard.html"
    context_object_name = 'tasks'

    def get_queryset(self):
        type=self.request.GET.get('type','all')
        queryset = Task.objects.select_related('details').prefetch_related('assigned_to')

        if type=='completed':
            return queryset.filter(status='COMPLETED')
        if type =='in-progress':
            return queryset.filter(status='IN_PROGRESS')
        if type == 'pending':
            return queryset.filter(status='PENDING')
        elif type =='all':
            return queryset.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts=Task.objects.aggregate(
            total=Count('id'),
            completed=Count('id',filter=Q(status="COMPLETED")),
            in_progress=Count('id',filter=Q(status="IN_PROGRESS")),
            pending=Count('id',filter=Q(status="PENDING")),
            )
        context['counts'] = counts
        context['role'] = 'Manager'
        context['type'] = self.request.GET.get('type','all')
        return context
        

"""
@user_passes_test(is_manager,login_url='no-permission')
def manager_dashboard(request):

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
        "counts":counts,
        "role":'manager'
    }
    return render(request,"dashboard/manager-dashboard.html",context)
"""
    

@method_decorator(user_passes_test(is_employee, login_url='no-permission'), name='dispatch')
class EmployeeView(ListView):
    model = Task
    template_name = "dashboard/user_dashboard.html"
    context_object_name = 'tasks'
    
    def get_queryset(self):
        type=self.request.GET.get('type','all')
        queryset = Task.objects.select_related('details').prefetch_related('assigned_to')

        if type=='completed':
            return queryset.filter(status='COMPLETED')
        if type =='in-progress':
            return queryset.filter(status='IN_PROGRESS')
        if type == 'pending':
            return queryset.filter(status='PENDING')
        elif type =='all':
            return queryset.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts=Task.objects.aggregate(
            total=Count('id'),
            completed=Count('id',filter=Q(status="COMPLETED")),
            in_progress=Count('id',filter=Q(status="IN_PROGRESS")),
            pending=Count('id',filter=Q(status="PENDING")),
            )
        context['counts'] = counts
        context['role'] = 'Employee'
        context['type'] = self.request.GET.get('type','all')
        return context


"""
@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request,"dashboard/user_dashboard.html")


@login_required
@permission_required('tasks.add_task',login_url='no-permission')
def create_task(request):
    # employees=Employee.objects.all()
    task_form=TaskModelForm()
    task_detail_form=TaskDetailModelForm()
    if request.method == "POST":
        task_form=TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST,request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():

            For Model Form Data 
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request,"Task Created Successfully")

            return redirect('create-task') 

           
    context={"task_form": task_form,"task_detail_form":task_detail_form}
    return render(request,"task_form.html",context)
"""

decorators = [login_required,permission_required('tasks.add_task',login_url='no-permission')]

class CreateTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'tasks.add_task'
    login_url = 'sign-in'
    template_name='task_form.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form']=kwargs.get('task_form',TaskModelForm())
        context['task_detail_form'] = kwargs.get('task_detail_form',TaskDetailModelForm())
        return context

    def get(self,request,*args, **kwargs):
       
        context=self.get_context_data()
        return render(request,self.template_name,context)
    
    def post(self,request,*args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST,request.FILES)
        
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail =task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request,"Task Created Successfully")
            context = self.get_context_data(task_form=task_form,task_detail_form=task_detail_form)

            return render(request,self.template_name,context)


"""
@login_required
@permission_required('tasks.change_task',login_url='no-permission')
def update_task(request,id):
    task=Task.objects.get(id=id)
    # employees=Employee.objects.all()
    task_form=TaskModelForm(instance=task)
    if task.details:
        task_detail_form=TaskDetailModelForm(instance=task.details)
    if request.method == "POST":
        task_form=TaskModelForm(request.POST,instance=task)
        task_detail_form=TaskDetailModelForm(request.POST,request.FILES,instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():

             For Model Form Data 
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request,"Task updated Successfully")

            return redirect('update-task',id)

    context={"task_form": task_form,"task_detail_form":task_detail_form}
    return render(request,"task_form.html",context)

"""

class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = "task_form.html"
    context_object_name = 'task'
    
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['task_form'] = self.get_form()

        if hasattr(self.object,'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(instance=self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()    

        return context
    
    def post(self,request,*args, **kwargs):
        self.object =self.get_object()
        task_form = TaskModelForm(request.POST,instance = self.object)
        task_detail_form = TaskDetailModelForm(request.POST,request.FILES,instance=getattr(self.object,'details',None))
        
        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request,"Task updated Successfully")

            return redirect('update-task',self.object.id)
        
        return redirect('update-task',self.object.id)


class DeleteTask(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Task
    template_name = "task_details.html"
    permission_required = "tasks.delete_task"
    login_url="no-permission"
    success_url = reverse_lazy("manager-dashboard")
    pk_url_kwarg = 'id'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Task Delete Successfully")
        return super().delete(request, *args, **kwargs)
    

"""
@login_required
@permission_required('tasks.delete_task',login_url='no-permission')
def delete_task(request,id):
    if request.method == 'POST':
        task=Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task Delete Successfully")
        return redirect('manager-dashboard')
    else:
        messages.error(request,"Something went wrong")
        return redirect('manager-dashboard')
      

@login_required
@permission_required('tasks.view_task',login_url='no-permission')
def view_task(request):   
    projects = Project.objects.annotate(
        num_task = Count('task')).order_by('num_task')
    return render(request,"show_task.html",{'projects':projects})
"""  

view_project_decorators = [login_required,permission_required('projects.view_projects',login_url='sign-in')]
@method_decorator(view_project_decorators,name='dispatch')
class ViewProject(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'show_task.html'

    def get_queryset(self):
        queryset = Project.objects.annotate(
        num_task = Count('task')).order_by('num_task')
        return queryset

#function type view
@login_required
@permission_required('tasks.view_task',login_url='no-permission')
def task_details(request,task_id):
    task=Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES

    if request.method == 'POST':
         selected_status = request.POST.get('task_status')
         task.status = selected_status
         task.save()
         return redirect('task-details',task.id)
    return render(request,'task_details.html',{'task':task,'status_choices':status_choices})


#class type view
class TaskDetail(DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices']=Task.STATUS_CHOICES
        return context
    
    def post(self,request,*args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details',task.id)

class UserTaskDetailView(DetailView):
    model = Task
    template_name = 'user_task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)



@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect("user-dashboard")
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    return redirect('no-permission')

