from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import Group
from users.forms import CustomRegistrationForm,EditProfileForm,CustomPasswordResetConfirmForm,CustomRegistrationForm,AssignRoleForm,CreateGroupForm,CustomPasswordResetForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView,PasswordResetView,PasswordResetConfirmView
from django.views.generic import TemplateView,ListView,UpdateView,FormView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

User = get_user_model()


#Test for users
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def sign_up(request):
    # if request.method == "GET":
    form=CustomRegistrationForm()  
    if request.method == "POST":
        form=CustomRegistrationForm(request.POST)
        if form.is_valid():   
           
            user=form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request,"A confirmation mail sent. Please check your mail")
            return redirect('sign-in')
        else :
            print("Form is not valid")          
    return render(request,'registration/register.html',{'form':form})

def sign_in(request):
   form=LoginForm()
   if request.method == 'POST':
       form= LoginForm(data=request.POST)
       if form.is_valid(): 
            user = form.get_user() 
            login(request,user)
            return redirect('home')
       
   return render(request,'registration/login.html',{'form':form})

class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

@login_required
def sign_out(request):
    logout(request)
    return redirect('sign-in')


def activate_user(request,user_id,token):
    try:
            user = User.objects.get(id=user_id)
            if default_token_generator.check_token(user,token):
                user.is_active = True
                user.save()
                return redirect('sign-in')
            else:
                return HttpResponse("Invalid id or token")
    except User.DoesNotExist:
        return HttpResponse("User not found")        

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'

    return render(request, 'admin/dashboard.html', {'users': users})


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('auth.change_user', login_url='no-permission'), name='dispatch')
class AssignRoleView(FormView):
    template_name = "admin/assign_role.html"
    form_class = AssignRoleForm
    
    def dispatch(self, request, *args, **kwargs):
        self.user=User.objects.get(id=self.kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        role = form.cleaned_data.get('role')
        self.user.groups.clear()
        self.user.groups.add(role)
        messages.success(self.request,f"User {self.user.username} has been assigned to the {role.name} role")
        return redirect('admin-dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user']=User
        return context

"""
@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request,user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm(request.POST)

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  #Removed old roles
            user.groups.add(role)
            messages.success(request,f"User {user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')
    return render(request,'admin/assign_role.html',{'form':form})    



@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group=form.save()
            messages.success(request,f'Group {group.name} has been created successfully')
            return redirect('create-group')

    return render(request,'admin/create_group.html',{'form':form})    
"""

@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class CreateGroup(CreateView):
    model = Group
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy('create-group')

    def form_valid(self, form):
        alamin = super().form_valid(form)
        messages.success(self.request, f"Group '{form.instance.name}' has been created successfully.")
        return alamin

@method_decorator(user_passes_test(is_admin,login_url='no-permission'),name='dispatch')
class GroupListView(ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()
     


"""
@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render (request,'admin/group_list.html',{'groups':groups})
"""


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context
    
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request,"A reset email sent.Please Check your Email")
        return super().form_valid(form)
    

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request,"Password Reset Successfully")
        return super().form_valid(form)
    
"""   
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user = self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user = self.request.user)
        context['form'] = self.form_class(instance=self.object,userprofile = user_profile)
        return context
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
"""

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')