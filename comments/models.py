# comments/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(upload_to='comment_attachments/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Generic relation to Goal, Outcome, Output, Indicator, etc.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Comment by {self.author} on {self.related_object}"
    def get_absolute_url(self):
        return f"/comments/{self.id}/"
    def get_attachment_url(self):
        if self.attachment:
            return self.attachment.url
        return None
    def get_author_name(self):
        return self.author.get_full_name() or self.author.username
    def get_author_email(self):
        return self.author.email
    def get_content_type_name(self):
        return self.content_type.model_class().__name__ if self.content_type else None
