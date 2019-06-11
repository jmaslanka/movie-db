from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Movie, Comment


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year', 'created_at',)
    list_filter = ('released',)
    search_fields = ('title',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_id', 'get_short_text', 'created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def get_short_text(self, obj):
        text = obj.text[:30]
        return text if len(text) <= 30 else f'{text}...'
    get_short_text.short_description = _('Text')


admin.site.register(Movie, MovieAdmin)
admin.site.register(Comment, CommentAdmin)
