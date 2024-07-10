from django.shortcuts import render, redirect, get_object_or_404
from home.models import Contact, Category, Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, ProductForm


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

@login_required
def categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories') 
    else:
        form = CategoryForm()
    categories = Category.objects.all()
    return render(request, 'categories.html', {'form': form, 'categories': categories})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('categories')

def products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()

    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products.html', {'form': form, 'products': products, 'categories': categories})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('products')