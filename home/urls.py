from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name='index'),
    path("contact/", views.contact, name='contact'),
    path("login/", views.loginUser, name='login'),
    path("logout/", views.logoutUser, name='logout'),
    path("categories/", views.categories, name='categories'),
    path("categories/delete/<int:category_id>/", views.delete_category, name='delete_category'),
    path("products/", views.products, name='products'),
    path("products/delete/<int:product_id>/", views.delete_product, name='delete_product'),
]
