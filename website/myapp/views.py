from django.shortcuts import render
from django.http import Http404
from .tmdb import TMDBService
from .utils import fetch_random_movies
import google.generativeai as genai
import requests


def home(request):
    api_key = "72dc4ec4984b317e678801598d3a5b59"

    random_movies = fetch_random_movies(api_key, count=18)
    return render(request, 'main/home.html', {'movies': random_movies})

def films_view(request):
    query = request.GET.get('query', '')
    movies = []
    if query:
        try:
            tmdb_response = TMDBService.get_movies(query)
            all_movies = tmdb_response.get('results', [])

            movies = [movie for movie in all_movies if movie.get('poster_path')]
        except Exception as e:
            print(f"Error fetching movies: {e}")

    return render(request, 'Film/films.html', {"movies": movies})


def movie_details_view(request, movie_id):
    API_KEY = "72dc4ec4984b317e678801598d3a5b59"

    # URL to fetch movie details and similar movies
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits,images"
    similar_url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={API_KEY}"

    try:
        # Fetch movie details
        response = requests.get(details_url)
        if response.status_code != 200:
            raise Http404("Movie not found")
        movie = response.json()

        # Fetch similar movies
        similar_response = requests.get(similar_url)
        if similar_response.status_code == 200:
            similar_movies = similar_response.json().get("results", [])[:6]  # Limit to 6 similar movies
        else:
            similar_movies = []

        # Fetch movie credits and images
        crew = movie.get('credits', {}).get('crew', [])
        cast = movie.get('credits', {}).get('cast', [])
        director = next((person['name'] for person in crew if person['job'] == 'Director'), 'Unknown')
        actors = [actor['name'] for actor in cast[:5]]  # Limit to top 5 actors
        images = movie.get('images', {}).get('backdrops', [])

        # Build context for the template
        context = {
            'title': movie.get('title', 'Unknown'),
            'poster_path': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}",
            'release_date': movie.get('release_date', 'Unknown'),
            'overview': movie.get('overview', 'No overview available.'),
            'rating': movie.get('vote_average', 'N/A'),
            'director': director,
            'actors': actors,
            'images': [f"https://image.tmdb.org/t/p/w500{img['file_path']}" for img in images],
            'similar_movies': similar_movies,  # Include similar movies in context
        }

        return render(request, 'Film/movie_details.html', context)

    except Exception as e:
        # Handle errors
        print(f"Error fetching movie details: {e}")
        raise Http404("Movie not found")

def books_view(request):
    query = request.GET.get('query', '')
    books = []

    if query:
        url = f"https://openlibrary.org/search.json?title={query}"
        response = requests.get(url)
        if response.status_code == 200:
            books_data = response.json().get("docs", [])
            books = [
                {
                    "id": book.get("key", '').split('/')[-1],  # Extract the book id from 'key'
                    "title": book.get("title", "Unknown Title"),
                    "author": book.get("author_name", ["Unknown Author"])[0],
                    "publish_year": book.get("first_publish_year", "N/A"),
                    "cover_image": f"https://covers.openlibrary.org/b/id/{book.get('cover_i', '')}-L.jpg" if book.get("cover_i") else None,
                }
                for book in books_data
            ]

    return render(request, 'Book/books.html', {'books': books})


def book_details_view(request, book_id):
    API_KEY = "AIzaSyBySoTz0PG6-poXTfa5yuKUrnsi00kYuBI"

    # API endpoint for fetching book details by book_id
    details_url = f"https://www.googleapis.com/books/v1/volumes/{book_id}?key={API_KEY}"

    try:
        # Fetch book details from the API
        response = requests.get(details_url)
        if response.status_code != 200:
            raise Http404("Book not found")
        book = response.json()

        # Build context for the template
        context = {
            'title': book.get('volumeInfo', {}).get('title', 'Unknown'),
            'author': ', '.join(book.get('volumeInfo', {}).get('authors', ['Unknown'])),
            'description': book.get('volumeInfo', {}).get('description', 'No description available.'),
            'cover_image': book.get('volumeInfo', {}).get('imageLinks', {}).get('thumbnail', ''),
            'published_date': book.get('volumeInfo', {}).get('publishedDate', 'Unknown'),
            'rating': book.get('volumeInfo', {}).get('averageRating', 'N/A'),
        }

        return render(request, 'Book/book_details.html', context)

    except Exception as e:
        print(f"Error fetching book details: {e}")
        raise Http404("Book not found")



def chatbot(request):
    # Configure the Gemini API
    genai.configure(api_key="AIzaSyDLt4gY92vond-GJohbUH6Bf9EmxwiYEX0")
    model = genai.GenerativeModel("gemini-1.5-flash")
    chatbot_response = None  # Default response

    if request.method == "POST":
        print("Form submitted!")  # Debugging print
        user_input = request.POST.get("user_input")  # Get user input from the form
        print(f"User input: {user_input}")  # Debugging print

        if user_input:
            try:
                # Generate a response using the Gemini model
                response = model.generate_content(user_input)
                chatbot_response = response.text.strip()  # Extract and clean up the response
                print(f"Chatbot response: {chatbot_response}")  # Debugging print
            except Exception as e:
                print(f"Error during Gemini API call: {e}")
                chatbot_response = "Sorry, something went wrong. Please try again later."

    # Render the response to the 'recommendations.html' template
    return render(request, 'recommendations.html', {'chatbot_response': chatbot_response})


def about(request):
    return render(request, 'about.html')

