from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView,
    ProjectCreateView, ProjectUpdateView, ProjectDeleteView, project_create_with_logframe
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project-edit'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('projects/create-full/', project_create_with_logframe, name='project-create-with-logframe'),

]
