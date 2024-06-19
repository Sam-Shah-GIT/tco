# ui/forms.py
from django import forms

class SimulationForm(forms.Form):
    COATING_MODELS = [
        # Add actual coating models here or load them dynamically
    ]
    CLEANING_OPTIONS = [
        ('Cleaning Frequency', 'Cleaning Frequency'),
        ('Fixed Cleanings', 'Fixed Cleanings'),
        ('Reactive Cleaning', 'Reactive Cleaning'),
    ]
    GROWTH_TYPES = [
        ('gaussian', 'Gaussian'),
        ('sigmoid', 'Sigmoid'),
        ('linear', 'Linear'),
    ]

    coating_model = forms.ChoiceField(choices=COATING_MODELS, required=True)
    cleaning_option = forms.ChoiceField(choices=CLEANING_OPTIONS, required=True)
    cleaning_frequency = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Cleaning Frequency (months)'}))
    growth_type = forms.ChoiceField(choices=GROWTH_TYPES, required=True)
    average_power = forms.FloatField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Average Power'}))
    max_speed = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Max Speed'}))
    activity = forms.FloatField(required=True, widget=forms.TextInput(attrs={'placeholder': '% Activity'}))
