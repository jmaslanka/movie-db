from json.decoder import JSONDecodeError
from typing import Union
import requests

from django.conf import settings

from .serializers import MovieSerializer


def fetch_movie(title: str) -> Union[None, dict]:
    """
    Given a movie title returns results (if any) from OMDB API.
    """

    url = '{base_url}?apikey={api_key}&type=movie&t={title}'.format(
        base_url=settings.OMDB_API_URL,
        api_key=settings.OMDB_API_KEY,
        title=title,
    )

    try:
        response = requests.get(
            url,
            headers={'user-agent': 'Movie DB'},
            timeout=1.5,
        )
        if not response.ok:
            return None

        data = response.json()
    except (requests.RequestException, JSONDecodeError):
        return None

    serializer = MovieSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data

    return None
