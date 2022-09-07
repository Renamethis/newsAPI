import sys
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from .models import News
from django.views import generic
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import News
from .serializers import NewsSerializer
import datetime
from json import loads
import logging

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = 'index.html'

# News model Viewset
class NewsViewset(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    # Endpoint which returns news by given date 
    @action(detail=False, methods=['get'], url_path="date", url_name="date")
    def date_news(self, request):
        news = News.objects.filter(pdate=datetime.datetime.strptime(request.GET.get('date'), "%d %B %Y"))
        return HttpResponse(serializers.serialize('json', news.all()), content_type='application/json')

    # Endpoint whivh returns news by given tags
    @action(detail=False, methods=['get'], url_path="tags", url_name="tags")
    def tags_news(self, request):
        tags = request.GET.get('tags').replace(" ", "").split(",")
        res = []
        for news in News.objects.all().values():
            tags_buf = tags.copy()
            amount = 0
            for tag in tags_buf:
                if(tag in news['tags']):
                    amount += 1
            if(len(tags_buf) == amount):
                res.append(news)
        return HttpResponse(res, content_type='application/json') 
