from store.admin import admin_site

from django.urls import path
from . import views

urlpatterns = [path('caradmin/', admin_site.urls),
               path('', views.home, name='home'),
               path('cars/', views.car_list, name='car_list'),
               path('cars/<int:pk>/', views.car_detail, name='car_detail'),
               ]
