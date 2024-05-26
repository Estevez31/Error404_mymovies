from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from movies.models import Movie, MovieReview, Genre, MovieCredit, Job, Person
from .forma import ReviewForm
from .reviewAll import ReviewMovie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from tmdbv3api import TMDb, People

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
    
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index') 
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'movies/login.html')
        
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index') 
    else:
        return redirect('index')
    
def movie_actors_view(request, movie_id, actor_name):
    movie = get_object_or_404(Movie, pk=movie_id)
    actor_job = get_object_or_404(Person, name=actor_name)
    actors = MovieCredit.objects.filter(movie=movie, person=actor_job).select_related('person')
    
    # Configurar TMDb
    tmdb = TMDb()
    tmdb.api_key = '706e6231b343905d4bcddfa6a6b91de9'
    
    # Buscar actor por nombre
    people = People()
    search_result = people.search_person(actor_name)
    
    # Obtener la URL de la imagen del primer resultado
    if search_result:
        actor_id = search_result[0].id
        actor_details = people.person_details(actor_id)
        actor_image_url = f"https://image.tmdb.org/t/p/w500{actor_details.profile_path}"
    else:
        actor_image_url = None
    
    return render(request, 'movies/movie_actors.html', {'movie': movie, 'actors': actors, 'actor_image_url': actor_image_url})