from django.urls import path
from reviews import views

urlpatterns = [
    path('', views.create_review_view, name="create_review"),
]
