from django_filters import rest_framework as filters

from .models import Movie


class MovieFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    year = filters.NumberFilter(field_name='released', lookup_expr='year')
    rated = filters.MultipleChoiceFilter(
        choices=Movie.PG_RATING_CHOICES,
        lookup_expr='iexact',
    )
    language = filters.CharFilter(lookup_expr='icontains')
    country = filters.CharFilter(lookup_expr='icontains')
    rating = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = (
            'title',
            'year',
            'rated',
            'language',
            'country',
            'rating',
        )
