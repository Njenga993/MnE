from django.urls import path
from .views import CommentListCreateView, CommentDetailView, comment_ui_view

urlpatterns = [
    path('', CommentListCreateView.as_view(), name='comment-list-create'),
    path('detail/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('<str:model_name>/<int:object_id>/', comment_ui_view, name='comment-ui'),
]
