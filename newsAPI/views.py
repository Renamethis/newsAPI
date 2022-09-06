from django.shortcuts import render
from django.views import generic
from rest_framework import viewsets
from .models import News
from .serializers import NewsSerializer

class IndexView(generic.TemplateView):
    template_name = 'index.html'

# News model Viewset
class NewsViewset(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
