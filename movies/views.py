from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from movies.models import Movie, MovieReview, Genre
from .forma import ReviewForm
from .reviewAll import ReviewMovie
from django.contrib.auth.models import User

def review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_instance = form.save(commit=False)
            review_instance.user = request.user
            review_instance.movie = movie
            review_instance.save()
            return redirect('movie_detail', movie_id=movie.id) 
    else:
        form = ReviewForm()
    return render(request, "movies/opinion.html", {'form': form, 'movie': movie})

def index(request):
    movies = Movie.objects.all()
    context = {'movie_list': movies}
    return render(request, "movies/index.html", context=context)

def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    reviews = MovieReview.objects.get(pk=movie_id) 
    context = {'movie': movie, 'reviews': reviews}  
    return render(request, "movies/movie_detail.html", context=context)

def get_movie_title(movie_id):
    movie = Movie.objects.get(pk=movie_id)
    return movie.title

def ReviewMovie(request, movie_id):
    review = MovieReview.objects.get(pk=movie_id)
    movie = Movie.objects.get(pk=movie_id)
    movie_title = get_movie_title(movie_id)
    reviews = MovieReview.objects.filter(movie__title=movie_title)
    context = {'movie': movie, 'reviews': reviews, 'review': review}  
    return render(request, "movies/allReview.html", context=context)