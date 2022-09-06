from django.urls import include,path
from rest_framework.routers import DefaultRouter
from newsAPI.views import NewsViewset

router = DefaultRouter()
router.register(r'news', NewsViewset, basename='news')

urlpatterns = [
    path('', include('newsAPI.urls')),
    *router.urls,
]