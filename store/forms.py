# forms.py
from django import forms
from .models import Review, Car

class ReviewForm(forms.ModelForm):
    """Form for submitting car reviews"""
    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }

class CarSearchForm(forms.Form):
    """Form for searching and filtering cars"""
    q = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={'placeholder': 'Search cars...'})
    )
    price_min = forms.DecimalField(
        required=False,
        label='Min Price',
        min_value=0
    )
    price_max = forms.DecimalField(
        required=False,
        label='Max Price',
        min_value=0
    )
    manufacturer = forms.ModelChoiceField(
        required=False,
        queryset=None,
        label='Manufacturer',
        empty_label='All Manufacturers'
    )
    fuel_type = forms.ChoiceField(
        required=False,
        choices=[],  # Will be populated in __init__
        label='Fuel Type',
    )
    available = forms.BooleanField(
        required=False,
        initial=True,
        label='Available Only'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the queryset for manufacturer field
        from .models import Manufacturer, Car
        self.fields['manufacturer'].queryset = Manufacturer.objects.all()
        
        # Get unique fuel types for the choices
        fuel_types = Car.objects.values_list('fuel_type', flat=True).distinct()
        self.fields['fuel_type'].choices = [('', 'All Fuel Types')] + [(ft, ft) for ft in fuel_types]