from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib import messages
from users.models import User
from products.models import Product


from .forms import RegisterForm


def index(request):
    products = Product.objects.all().order_by('-id')
    return render(request,'index.html',{
        'products':products
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            messages.success(request,'Bienvenido {}'.format(user.username))

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])

            return redirect('index')
        else:
            messages.error(request,'Usuario o Contraseña incorrecto')

    return render(request,'users/login.html',{})

def logout_view(request):
    logout(request)
    messages.success(request,'Sesion cerrada exitosamente')
    return redirect('login')

def register(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user:
            messages.success(request,'Te has registrado exitosamente')
            return redirect('index')

    return render(request,'users/register.html',{'form':form})