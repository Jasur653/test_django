from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_movement_list, name='stock_movement_list'),
    path('create/', views.stock_movement_create, name='stock_movement_create'),
    path('<int:pk>/', views.stock_movement_detail, name='stock_movement_detail'),
]