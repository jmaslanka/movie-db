from django.urls import include, path

from rest_framework import routers

from .views import TopMoviesListView
from .viewsets import (
    CommentViewSet,
    MovieViewSet,
)


router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'comments', CommentViewSet)

app_name = 'movie'
urlpatterns = [
    path('', include(router.urls)),
    path('top/', TopMoviesListView.as_view(), name='top-movies'),
]
