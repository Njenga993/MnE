from rest_framework import serializers
from .models import Comment
from django.contrib.contenttypes.models import ContentType

class CommentSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'content', 'timestamp', 'content_type', 'object_id']
        read_only_fields = ['id', 'timestamp', 'author']
        extra_kwargs = {
            'content': {'required': True},
            'object_id': {'required': True}
        }