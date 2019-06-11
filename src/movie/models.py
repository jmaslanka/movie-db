from django.db import models
from django.utils.translation import gettext_lazy as _


class Movie(models.Model):
    PG_RATING_CHOICES = [
        ('G', 'G'),
        ('PG', 'PG'),
        ('PG-13', 'PG-13'),
        ('R', 'R'),
        ('NC-17', 'NC-17'),
    ]

    title = models.CharField(
        _('title'),
        max_length=200,
    )
    released = models.DateField(
        _('release date'),
    )
    rated = models.CharField(
        _('PG rating'),
        max_length=5,
        choices=PG_RATING_CHOICES,
        blank=True,
        null=True,
    )
    runtime = models.PositiveSmallIntegerField(
        _('runtime'),
        blank=True,
        null=True,
    )
    genre = models.CharField(
        _('genre'),
        max_length=100,
        blank=True,
    )
    director = models.CharField(
        _('director'),
        max_length=80,
        blank=True,
    )
    writer = models.CharField(
        _('writer'),
        max_length=255,
        blank=True,
    )
    actors = models.CharField(
        _('actors'),
        max_length=255,
        blank=True,
    )
    plot = models.CharField(
        _('plot'),
        max_length=255,
        blank=True,
    )
    language = models.CharField(
        _('language'),
        max_length=100,
        blank=True,
    )
    country = models.CharField(
        _('country'),
        max_length=100,
        blank=True,
    )
    awards = models.CharField(
        _('awards'),
        max_length=100,
        blank=True,
    )
    rating = models.DecimalField(
        _('rating'),
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
    )
    box_office = models.PositiveIntegerField(
        _('box office'),
        blank=True,
        null=True,
    )
    production = models.CharField(
        _('production'),
        max_length=100,
        blank=True,
    )
    website = models.URLField(
        _('website'),
        blank=True,
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
    )

    @property
    def year(self):
        return self.released.year

    class Meta:
        verbose_name = _('movie')
        verbose_name_plural = _('movies')

    def __str__(self):
        return f'{self.title} ({self.year})'


class Comment(models.Model):

    movie = models.ForeignKey(
        Movie,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('movie'),
        related_name='comments',
    )
    text = models.TextField(
        _('text'),
        max_length=500,
    )
    created_at = models.DateTimeField(
        'created at',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return f'{self.text[:15]}... (Movie ID: {self.movie_id})'
