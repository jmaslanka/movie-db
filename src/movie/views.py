from datetime import datetime

from django.db.models import Count, Window, F, Q
from django.db.models.functions import DenseRank

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Movie
from .serializers import TopMovieSerializer


class TopMoviesListView(ListAPIView):
    serializer_class = TopMovieSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def get_queryset(self, date_from, date_to):
        return Movie.objects.annotate(
            total_comments=Count(
                'comments',
                filter=Q(
                    comments__created_at__range=[date_from, date_to],
                ),
            ),
            rank=Window(
                expression=DenseRank(),
                order_by=F('total_comments').desc(),
            ),
        ).order_by('rank')

    def list(self, request, *args, **kwargs):
        try:
            date_from = datetime.strptime(
                request.query_params['from'],
                '%d-%m-%Y',
            ).date()
            date_to = datetime.strptime(
                request.query_params['to'],
                '%d-%m-%Y',
            ).date()
        except (ValueError, KeyError):
            error_msg = '`from` and `to` date required in format "DD-MM-YYY"'
            return Response(
                {'error': error_msg},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset(date_from, date_to)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
