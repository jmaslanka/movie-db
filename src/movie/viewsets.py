from django_filters import rest_framework as filters

from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filters import MovieFilter
from .models import Movie, Comment
from .serializers import (
    CommentSerializer,
    MovieSerializer,
    MovieSearchSerializer,
)
from .utils import fetch_movie


class MovieViewSet(
        GenericViewSet,
        CreateModelMixin,
        ListModelMixin):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []
    paginator = None
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_class = MovieFilter
    ordering_fields = ('released', 'runtime', 'box_office', 'rating',)

    def create(self, request, *args, **kwargs):
        serializer = MovieSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            movie = Movie.objects.get(
                title__iexact=serializer.data.get('title')
            )
            return Response(
                MovieSerializer(movie).data,
                status=status.HTTP_200_OK,
            )
        except Movie.DoesNotExist:
            pass

        movie_data = fetch_movie(serializer.data.get('title'))

        if movie_data:
            return Response(
                movie_data,
                status=status.HTTP_201_CREATED,
            )

        return Response(status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(
        GenericViewSet,
        CreateModelMixin,
        ListModelMixin):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []
    paginator = None
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('movie',)
