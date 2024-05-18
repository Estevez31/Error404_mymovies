from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from movies.models import Movie, MovieReview
from .forms import NameForm 
from .forma import ReviewForm
from .reviewAll import ReviewMovie
from django.contrib.auth.models import User

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data)
            # ...
            # redirect to a new URL:
            return render(request, "movies/name_ok.html", {"form": form})
        else:
            return render(request, "movies/name_ok.html", {"form": form})
            
        # if a GET (or any other method) we'll create a black form
    else:
        form = NameForm()
        
    return render(request, "movies/name.html", {"form": form})

def review(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    context = {'movie': movie}
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            review = form.changed_data['review']
            MovieReview.objects.create(user=request.user, movie=movie, rating=rating, review=review)
            return redirect("movies/opinion.html", {'form': form})
    else:
        form = ReviewForm() 
    return render(request, "movies/opinion.html", {'form': form, "movie_id": movie_id})

def index(request):
    movies = Movie.objects.all()
    context = {'movie_list': movies}
    return render(request, "movies/index.html", context=context)
    #return HttpResponse(movies)


def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    reviews = MovieReview.objects.get(pk=movie_id) # Obtener las reseñas asociadas con la película
    context = {'movie': movie, 'reviews': reviews}  # Pasar la película y las reseñas al contexto
    return render(request, "movies/movie_detail.html", context=context)

def ReviewMovie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)  # Obtener la película con el ID proporcionado
    reviews = MovieReview.objects.filter(pk=movie_id) # Obtener las reseñas asociadas con la película
    context = {'movie': movie, 'reviews': reviews}  # Pasar la película y las reseñas al contexto
    return render(request, "movies/allReview.html", context=context)
