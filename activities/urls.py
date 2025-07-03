from django.urls import path
from . import views

urlpatterns = [
    path('', views.activity_list, name='activity-list'),
    path('create/', views.activity_create, name='activity-create'),
    path('edit/<int:pk>/', views.activity_update, name='activity-edit'),
    path('delete/<int:pk>/', views.activity_delete, name='activity-delete'),
]
