from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('create/', views.supplier_create, name='supplier_create'),
    path('<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('<int:pk>/update/', views.supplier_update, name='supplier_update'),
    path('<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
    path('restocks/', views.restock_list, name='restock_list'),
    path('restocks/create/', views.restock_create, name='restock_create'),
    path('restocks/<int:pk>/update/', views.restock_update, name='restock_update'),
    path('restocks/<int:pk>/delete/', views.restock_delete, name='restock_delete'),
]