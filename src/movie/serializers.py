import re

from rest_framework import serializers

from .models import Movie, Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'movie',
            'text',
        )


class MovieSearchSerializer(serializers.Serializer):
    title = serializers.CharField()


class TopMovieSerializer(serializers.ModelSerializer):
    total_comments = serializers.IntegerField()
    rank = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'total_comments',
            'rank',
        )


class MovieSerializer(serializers.ModelSerializer):
    released = serializers.DateField(input_formats=['%d %b %Y'])

    def to_internal_value(self, data):
        # Keys are capitalized so we make them lowercase
        data = {k.lower(): v for k, v in data.items() if v != 'N/A'}

        # Rename input fields to match our model
        data['box_office'] = data.pop('boxoffice', None)
        data['rating'] = data.pop('imdbrating', None)

        # Get value from string and format it to match our model
        box_office = re.search('\d+(?:,\d+)+', data.get('boxoffice', ''))
        runtime = re.search('\d+', data.get('runtime', ''))

        if box_office:
            data['box_office'] = int(box_office.group().replace(',', ''))

        if runtime:
            data['runtime'] = int(runtime.group())

        return super().to_internal_value(data)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'released',
            'rated',
            'runtime',
            'genre',
            'director',
            'writer',
            'actors',
            'plot',
            'language',
            'country',
            'awards',
            'rating',
            'box_office',
            'production',
            'website',
        )
