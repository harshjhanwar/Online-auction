from django import forms
from .models import *

class NewListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid','c', 'image']
        labels = {"c":"Category"}

        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control'}),
            'description' : forms.Textarea(attrs={'class' : 'form-control', 'rows' : 4, 'columns':40}),
            'starting_bid' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'c' : forms.TextInput(attrs={'class' : 'form-control'}),
            'image' : forms.URLInput(attrs={'class' : 'form-control'}),    
        }
