from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from movies.models import Movie, MovieReview, Genre, MovieCredit, Job, Person
from .forma import ReviewForm
from .reviewAll import ReviewMovie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import requests

api_key = 'api'

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
    
    # Obtener todas las películas disponibles
    all_movies = Movie.objects.exclude(pk=movie_id)
    
    # Filtrar las películas recomendadas excluyendo la película consultada
    recommended_movies = all_movies[:11] 
    
    context = {'movie': movie, 'reviews': reviews, 'recommended_movies': recommended_movies}  
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
   # Obtén el objeto de la película y el actor de la base de datos
    movie = get_object_or_404(Movie, pk=movie_id)
    actor_job = get_object_or_404(Person, name=actor_name)
    actors = MovieCredit.objects.filter(movie=movie, person=actor_job).select_related('person')
    
    # Endpoint para buscar personas en TMDb
    url_busqueda = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor_name}"

    # Realizar la solicitud de búsqueda a TMDb
    respuesta_busqueda = requests.get(url_busqueda)
    datos_busqueda = respuesta_busqueda.json()
    
    actor_image_url = None
    actor_biography = None
    
    if 'results' in datos_busqueda and datos_busqueda['results']:
        # Tomar el primer resultado de la búsqueda
        actor = datos_busqueda['results'][0]
        actor_id = actor.get('id')
        perfil_path = actor.get('profile_path')
        
        if perfil_path:
            # Construir la URL completa de la imagen del perfil
            actor_image_url = f"https://image.tmdb.org/t/p/w500{perfil_path}"
        
        # Obtener más detalles del actor incluyendo la biografía
        url_detalle_actor = f"https://api.themoviedb.org/3/person/{actor_id}?api_key={api_key}"
        respuesta_detalle_actor = requests.get(url_detalle_actor)
        datos_detalle_actor = respuesta_detalle_actor.json()
        
        actor_biography = datos_detalle_actor.get('biography')
    
    context = {
        'movie': movie,
        'actors': actors,
        'actor_image_url': actor_image_url,
        'actor_biography': actor_biography,
    }
    
    return render(request, 'movies/movie_actors.html', context)
