from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import RegisterUserForm
from contabilidad.models import Propietario

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username = username,password = password,)
        if user is not None:
            login(request,user)
            return redirect('conta:transaccion-lista')
        else:
            messages.error(request,("Lo sentimos, las credenciales que ingresaste no son correctas. Por favor, verifica tu nombre de usuario y contraseña e inténtalo de nuevo."))
            return redirect('login')

    else:
        return render(request,'registration/login.html')

def register_user(request):
    context = {}
    if request.method == "POST":
        register_form = RegisterUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            Propietario.objects.create(user=user)
            return redirect('login')
        else:
            context['form'] = register_form
            messages.error(request,("Lo sentimos, no fue posible registrarte con estas credenciales. Por favor, intentalo nuevamente con otras credenciales"))
            return render(request,'registration/sign_up.html',context)
            
    else:
        context['form'] = RegisterUserForm()

    return render(request,'registration/sign_up.html',context)

        


