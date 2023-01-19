from django.urls import path
from base import views

urlpatterns = [
    path('', views.products_list, name='home'),
    path('register/', views.register, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('products/<int:pk>/', views.product_detail, name="product_detail"),

    # STAFF FUNCTIONALITY URLS
    path('create-product/', views.create_product, name="create_product"),
    path('edit-product/<int:pk>/', views.edit_product, name="edit_product"),
    path('remove-product/<int:pk>/', views.remove_product, name="remove_product"),
    path('staff/products/', views.staff_products_list, name='staff_products_view'),
    path('staff/users/', views.staff_users_list, name='staff_users_view'),
    path('staff/users/<int:pk>/', views.staff_show_user_detail, name='show_user_details'),

]
