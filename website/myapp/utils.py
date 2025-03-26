import requests
import random

def fetch_random_movies(api_key, count=5):
    # Fetch popular movies
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {
        "api_key": api_key,
        "language": "en-US",
        "page": random.randint(1, 500)  # Randomize the page to get different movies
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        movies = response.json().get("results", [])
        # Randomly select the desired number of movies
        return random.sample(movies, min(count, len(movies)))
    else:
        return []
