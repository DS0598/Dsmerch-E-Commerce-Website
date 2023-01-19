from django.urls import path
from userprofile import views

urlpatterns = [
    path('', views.profile_page, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('create-address/', views.create_address, name='create_address'),
    path('edit-address/<int:pk>/', views.edit_address, name='edit_address'),
    path('default-address/<int:pk>/', views.make_default_address, name="make_default_address"),
    path('remove-address/<int:pk>/', views.remove_address, name="delete_address"),
]