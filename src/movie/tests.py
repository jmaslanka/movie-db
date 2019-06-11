from datetime import date, timedelta

from django.urls import reverse
from django.utils.http import urlencode

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Movie, Comment


class MovieTests(APITestCase):

    def setUp(self):
        self.movie1 = Movie.objects.create(
            title='Forrest Gump',
            released=date(1994, 6, 23),
            rated='PG',
            language='Spanish,English',
            country='USA,UK,New Zealand',
            rating=9.2,
        )
        self.movie2 = Movie.objects.create(
            title='The Matrix',
            released=date(1999, 3, 24),
        )
        self.base_movie_count = Movie.objects.count()
        self.url = reverse('movie:movie-list')

    def test_movie_list(self):
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.base_movie_count)

        # checking all filters

        url = '{}?{}'.format(
            self.url,
            urlencode({
                'year': self.movie1.year,
                'rated': self.movie1.rated,
                'language': self.movie1.language.split(',')[1],
                'country': self.movie1.country.split(',')[1],
                'rating_min': self.movie1.rating - 0.5,
                'rating_max': self.movie1.rating + 0.5,
            })

        )
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('title'), self.movie1.title)

    def test_add_movie(self):
        data = {'title': 'John Wick'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), self.base_movie_count + 1)

        # check already existing movie
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.count(), self.base_movie_count + 1)


class CommentTests(APITestCase):
    def setUp(self):
        self.movie1 = Movie.objects.create(
            title='The Matrix',
            released=date(1999, 3, 24),
        )
        self.movie2 = Movie.objects.create(
            title='Forrest Gump',
            released=date(1994, 6, 23),
        )
        self.comment1 = Comment.objects.create(
            movie=self.movie1,
            text='Good movie 1',
        )
        self.comment1.created_at = date(2019, 6, 6)
        self.comment1.save()

        self.comment2 = Comment.objects.create(
            movie=self.movie2,
            text='Good movie 2',
        )
        self.comment2.created_at = date(2019, 7, 7)
        self.comment2.save()

        self.base_comment_count = Comment.objects.count()
        self.url = reverse('movie:comment-list')

    def test_comment_list(self):
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.base_comment_count)

        response = self.client.get(
            f'{self.url}?movie={self.movie2.id}',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_add_comment(self):
        data = {'movie': self.movie1.id, 'text': 'Nice movie!'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), self.base_comment_count + 1)
        self.assertEqual(response.data.get('text'), 'Nice movie!')

    def test_top_movies(self):
        url = '{}?from={}&to={}'.format(
            reverse('movie:top-movies'),
            self.comment1.created_at.strftime('%d-%m-%Y'),
            self.comment2.created_at.strftime('%d-%m-%Y'),
        )
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Movie.objects.count())
        self.assertEqual(response.data[0]['rank'], response.data[1]['rank'])

        url = '{}?from={}&to={}'.format(
            reverse('movie:top-movies'),
            self.comment1.created_at.strftime('%d-%m-%Y'),
            (
                self.comment2.created_at - timedelta(days=2)
            ).strftime('%d-%m-%Y'),
        )
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Movie.objects.count())
        self.assertNotEqual(response.data[0]['rank'], response.data[1]['rank'])
