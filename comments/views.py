from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .serializers import CommentSerializer
from rest_framework import generics, permissions


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

    def get_object(self):
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        comment_id = self.kwargs.get('pk')

        if content_type and object_id and comment_id:
            try:
                ct = ContentType.objects.get(model=content_type)
                return Comment.objects.get(content_type=ct, object_id=object_id, id=comment_id)
            except (ContentType.DoesNotExist, Comment.DoesNotExist):
                return None
        return None
    

@login_required
def comment_ui_view(request, model_name, object_id):
    content_type = get_object_or_404(ContentType, model=model_name)
    target_object = content_type.get_object_for_this_type(id=object_id)

    if request.method == "POST":
        content = request.POST.get("content")
        attachment = request.FILES.get("attachment")

        if content.strip():
            Comment.objects.create(
                author=request.user,
                content=content,
                attachment=attachment,
                content_type=content_type,
                object_id=object_id
            )
        return redirect(request.path)

    comments = Comment.objects.filter(content_type=content_type, object_id=object_id).select_related("author")
    return render(request, "comments/comment_ui.html", {
        "comments": comments,
        "target_object": target_object
    })
@login_required
def comment_list_view(request, model_name, object_id):
    content_type = get_object_or_404(ContentType, model=model_name)
    target_object = content_type.get_object_for_this_type(id=object_id)

    comments = Comment.objects.filter(content_type=content_type, object_id=object_id).select_related("author")
    return render(request, "comments/comment_list.html", {
        "comments": comments,
        "target_object": target_object
    })
@login_required
def comment_delete_view(request, model_name, object_id, comment_id):
    content_type = get_object_or_404(ContentType, model=model_name)
    comment = get_object_or_404(Comment, id=comment_id, content_type=content_type, object_id=object_id)

    if request.user == comment.author:
        comment.delete()
        return redirect('comment-list', model_name=model_name, object_id=object_id)
    else:
        return render(request, "comments/error.html", {"message": "You do not have permission to delete this comment."})
@login_required
def comment_edit_view(request, model_name, object_id, comment_id):
    content_type = get_object_or_404(ContentType, model=model_name)
    comment = get_object_or_404(Comment, id=comment_id, content_type=content_type, object_id=object_id)

    if request.user != comment.author:
        return render(request, "comments/error.html", {"message": "You do not have permission to edit this comment."})

    if request.method == "POST":
        content = request.POST.get("content")
        attachment = request.FILES.get("attachment")

        if content.strip():
            comment.content = content
            if attachment:
                comment.attachment = attachment
            comment.save()
            return redirect('comment-list', model_name=model_name, object_id=object_id)

    return render(request, "comments/comment_edit.html", {
        "comment": comment,
        "target_object": content_type.get_object_for_this_type(id=object_id)
    })


