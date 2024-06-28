from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import Taskform
from .models import Task
from django.contrib.auth.decorators import login_required
from . import models
# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST ['password2']:
            try:
                user= User.objects.create_user(
                    username =request.POST['username'], password= request.POST
                    ['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'User already exists'
        })         
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Password do not match'
        })
  
def tasks(request):
    tasks=Task.objects.all()
    return render(request, 'tasks.html',{'tasks':tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': Taskform
    })
    else: 
        try:
            form = Taskform(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html',{
                'form': Taskform,
                'error': 'Please provide valida data'
            })
@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
        'form': AuthenticationForm
    })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'username or password is incorrect'
            })
        else:
            login(request,user)
            return redirect('tasks')
        
@login_required
def acciones(request):
    tasks=Task.objects.all()

    if request.method == 'GET':
        return render(request, 'tasks_acciones.html',{'tasks':tasks})
    else:
        tarea_id_delete= request.POST.get('tarea_id_delete')
        tarea_id_update= request.POST.get('tarea_id_update')

        identificador = request.POST.get('identificador')
        nombre_update = request.POST.get('nombre_update')
        print('----------')

        print(tarea_id_delete)
        print(tarea_id_update)

        print('--------------')

        if (tarea_id_delete):
            print(f"Eliminando datos: {tarea_id_delete}")

            eliminar_tarea = models.Task.objects.get(Codigo=tarea_id_delete)
            eliminar_tarea.delete()
            return render(request, 'tasks_acciones.html',{'tasks':tasks})
        elif (tarea_id_update):
            print(f"Actualizando datos: {tarea_id_update}")
            consulta = models.Task.objects.get(Codigo=tarea_id_update)
            print(consulta.Nombre)
            print(consulta.Creditos)
            context = {
                'task': consulta
            }
            return render(request, 'modificar_tasks_acciones.html',context)
        elif(identificador and nombre_update):
            print("Actualizando datos")
            print(f"identificador = {identificador}")
            print(f"nombre = {nombre_update}")
            consulta = models.Task.objects.get(Codigo=identificador)
            consulta.Nombre = nombre_update
            consulta.save()
            return redirect('acciones')
            
        return render(request, 'tasks_acciones.html',{'tasks':tasks})

