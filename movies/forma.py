from django import forms
from .models import MovieReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['rating', 'review']
        widgets = {'review': forms.Textarea(attrs={'rows': 2, 'cols': 22, 'class': 'text-gray-400'})}