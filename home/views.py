from django.shortcuts import render, redirect, get_object_or_404
from home.models import Contact, Category, Product, StockHistory  
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, ProductForm, StockHistoryForm
from django.utils import timezone
import pytz



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
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('products')

@login_required
def inventory(request):
    if request.method == 'POST':
        form = StockHistoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = StockHistoryForm()

    products = Product.objects.all()

    # Calculate current stock for each product
    for product in products:
        stock_in = StockHistory.objects.filter(product=product).aggregate(total_in=Sum('stock_in'))['total_in'] or 0
        stock_out = StockHistory.objects.filter(product=product).aggregate(total_out=Sum('stock_out'))['total_out'] or 0
        product.current_stock = product.quantity + stock_in - stock_out

    return render(request, 'inventory.html', {'form': form, 'products': products})


def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    stock_history = StockHistory.objects.filter(product=product).order_by('-date')

    if request.method == 'POST':
        form = StockHistoryForm(request.POST)
        if form.is_valid():
            stock_entry = form.save(commit=False)
            stock_entry.product = product
            stock_entry.date = timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
            stock_entry.save()
            return redirect('product_view', product_id=product.id)
    else:
        form = StockHistoryForm()

    # Calculate current stock
    stock_in_total = stock_history.aggregate(total_in=Sum('stock_in'))['total_in'] or 0
    stock_out_total = stock_history.aggregate(total_out=Sum('stock_out'))['total_out'] or 0
    current_stock = product.quantity + stock_in_total - stock_out_total

    # Prepare history data
    stock_entries = []
    temp_stock = product.quantity
    for entry in reversed(stock_history):
        stock_in = entry.stock_in or 0
        stock_out = entry.stock_out or 0
        temp_stock = temp_stock + stock_in - stock_out
        stock_entries.append({
            'date': entry.date.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'),  
            'quantity': temp_stock
        })

    # Reverse the order of stock entries to show the most recent first
    stock_entries.reverse()

    return render(request, 'product_view.html', {
        'product': product,
        'stock_entries': stock_entries,
        'current_stock': current_stock,
        'form': form,
    })

def stock_history_edit(request, history_id):
    stock_history = get_object_or_404(StockHistory, id=history_id)
    if request.method == 'POST':
        form = StockHistoryForm(request.POST, instance=stock_history)
        if form.is_valid():
            stock_entry = form.save(commit=False)
            stock_entry.date = stock_history.date.astimezone(pytz.timezone('Asia/Kolkata'))  # Ensure the date is saved in IST
            stock_entry.save()
            return redirect('product_view', product_id=stock_history.product.id)
    else:
        form = StockHistoryForm(instance=stock_history)
    return render(request, 'stock_history_edit.html', {'form': form})