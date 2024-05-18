from django import forms
from .models import MovieReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['rating', 'review']