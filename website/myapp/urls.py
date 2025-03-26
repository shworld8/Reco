from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('films/', views.films_view, name='films'),
    path('films/<int:movie_id>/', views.movie_details_view, name='movie_details'),
    path('books/', views.books_view, name='books'),
    path('book/<str:book_id>/', views.book_details_view, name='book_details'),
    path('recommendations/', views.chatbot, name='recommendations'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),

]