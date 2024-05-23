from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("movies/<int:movie_id>/allReview/", views.ReviewMovie, name="reviews"),
    path("movies/<int:movie_id>/opinion/", views.review, name="review"),
    path('movies/login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
]