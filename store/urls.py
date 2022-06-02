from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [path('', views.home, name='home'),
                path('cars/', views.car_list, name='car_list'),
                path('cars/<int:pk>/', views.car_detail, name='car_detail'),
                ]