from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Movie DB API',
        default_version='v1',
        description='API to fetch movie data.',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(),
)

docs_urlpatterns = [
    path(
        'docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger',
    ),
    path(
        'dock-redoc',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('movie.urls', namespace='movie')),
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
] + docs_urlpatterns
