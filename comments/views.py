# views.py for comments
from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer
from django.contrib.contenttypes.models import ContentType

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        if content_type and object_id:
            try:
                ct = ContentType.objects.get(model=content_type)
                return Comment.objects.filter(content_type=ct, object_id=object_id)
            except ContentType.DoesNotExist:
                return Comment.objects.none()
        return Comment.objects.none()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        if content_type and object_id:
            try:
                ct = ContentType.objects.get(model=content_type)
                return Comment.objects.filter(content_type=ct, object_id=object_id)
            except ContentType.DoesNotExist:
                return Comment.objects.none()
        return Comment.objects.none()
    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise permissions.PermissionDenied("You do not have permission to edit this comment.")
        serializer.save()
    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise permissions.PermissionDenied("You do not have permission to delete this comment.")
        instance.delete()
        
