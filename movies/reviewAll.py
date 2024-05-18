from django import forms
from .models import MovieReview

class ReviewMovie(forms.Form):
     class Meta:
        model = MovieReview
        fields = ['movie', 'rating', 'review']