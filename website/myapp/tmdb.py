import requests
from django.conf import settings

class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3"

    @staticmethod
    def get_movies(query):
        """Search movies by a query string."""
        endpoint = f"{TMDBService.BASE_URL}/search/movie"
        params = {
            "api_key": settings.TMDB_API_KEY,
            "query": query,
        }
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    @staticmethod
    def get_movie_details(movie_id):
        """Get details of a specific movie."""
        endpoint = f"{TMDBService.BASE_URL}/movie/{movie_id}"
        params = {
            "api_key": settings.TMDB_API_KEY,
        }
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
