# urls.py for comments
from django.urls import path
from .views import CommentListCreateView, CommentUIPage

urlpatterns = [
    path('', CommentListCreateView.as_view(), name='comment-list-create'),
     path('ui/', CommentUIPage.as_view(), name='comment-ui'),
]
