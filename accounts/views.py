from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import Student

# Create your views here.
def logout(request):
    auth_logout(request)
    return redirect('/')

def login(request):
    if request.user.is_superuser:
        return redirect('app/admin_view/')
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('app/')
        else:
            messages.info(request,'Invalid username or Password')
            return redirect('login')
    else:
        return render(request,"accounts/login.html")

def register(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['pass']
        username = request.POST['username']
        
        if User.objects.filter(email=email).exists():
            messages.info(request,'email already registered')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request,'Username already taken')
            return redirect('register')
        else:
            user = User(username=username,email=email,password=password)
            user.set_password(password)
            user.save()
            student = Student(user=user, flag=False)
            student.save()
            return redirect('login')
    else:
        return render(request,"accounts/register.html")
