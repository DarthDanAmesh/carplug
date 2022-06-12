from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content', 'rating')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Content', 'name': 'review'}),
            'rating': forms.NumberInput(attrs={'placeholder': 'Your Rating', 'name': 'rating'})
        }
