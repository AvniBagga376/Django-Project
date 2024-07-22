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
    path("delete_product/<int:product_id>/", views.delete_product, name='delete_product'),
    path("inventory/", views.inventory, name='inventory'),
    path("inventory/<int:product_id>/", views.product_view, name='product_view'),
    path("inventory/<int:history_id>/edit/", views.stock_history_edit, name='stock_history_edit'),
]
