from django.shortcuts import render, redirect
from home.models import Contact
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages




# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect('login')
    return render(request, 'index.html')
   # return HttpResponse("this is homepage")

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
             return render(request, 'login.html')
    return render(request, 'login.html')

def contact(request):
    if request.method == "POST":
        name= request.POST.get('name')
        phone= request.POST.get('phone')
        email= request.POST.get('email')
        desc= request.POST.get('desc')
        contact= Contact(name=name, phone=phone, email=email, desc=desc)
        contact.save()
        messages.success(request, "Your message has been sent!")
    return render(request, 'contact.html')

def logoutUser(request):
    logout(request)
    return redirect("login")
