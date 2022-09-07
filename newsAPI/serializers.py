from rest_framework import serializers
from .models import News

# News model serializer
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'uri', 'title', 'content', 'tags', 'pdate']
