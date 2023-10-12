from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.
def home(request):
    name_site = 'Home'
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ""
    return render(request, 'index.html',{
        'name_site': name_site,
        'username': username,
    })


def signup(request):
    name_site = 'SignUp'
    web_site = 'signup.html'
    if request.method == 'GET':
        return render(request, web_site,{
            'form': UserCreationForm,
            'name_site': name_site
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username = request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
            except IntegrityError:
                return render(request, web_site,{
                    'form': UserCreationForm,
                    'error': 'Username already in use',
                    'name_site': name_site
                })
        return render(request, web_site,{
            'form': UserCreationForm,
            'error': 'Password do not match',
            'name_site': name_site
        })
    

def signin(request):
    name_site = 'Login'
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'name_site': name_site,
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'name_site': name_site,
                'error': 'no user'
            })
        else:
            login(request, user)
            return redirect('task')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def tasks(request):
    name_site = 'Tasks'
    tasks = Task.objects.filter(user = request.user)
    return render(request, 'tasks.html',{
        'name_site': name_site,
        'tasks': tasks,
    })

@login_required
def task_details(request, task_id):
    name_site = 'Details'
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_details.html', {
            'task': task, 
            'form': form,
            'name_site': name_site,
            })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('task')
        except ValueError:
            return render(request, 'task_details.html', {'task': task, 'form': form, 'error': 'Error updating task.', 'name_site': name_site,})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.finishdate = timezone.now()
        task.save()
        return redirect('task')
    
@login_required
def undo_complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.finishdate = None
        task.save()
        return redirect('task')

    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')

@login_required
def create_task(request):
    name_site = 'Tasks'
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'name_site': name_site,
            'form': TaskForm, 
        })
    else:
       form = TaskForm(request.POST)
       new_task = form.save(commit=False)
       new_task.user =  request.user
       new_task.save()
       return redirect('task')
