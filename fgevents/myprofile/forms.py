from django import forms

class ProfileForm(forms.Form):
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'placeholder': 'Latitude'}))
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, widget=forms.NumberInput(attrs={'placeholder': 'Longitude'}))
    search_radius = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Search Radius'}))