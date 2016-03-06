from django.shortcuts import render, redirect
from django.contrib.auth.decorators import  login_required

from .forms import ProfileForm

# Create your views here.

@login_required
def index(request):
    user_lat = 0.0
    user_long = 0.0
    user_search_radius = 0
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            lat = form.cleaned_data['latitude']
            long = form.cleaned_data['longitude']
            search_radius = form.cleaned_data['search_radius']
            profile = request.user.profile
            profile.latitude = lat
            profile.longitude = long
            profile.find_radius = search_radius
            profile.save()
            return redirect("eventfeed-index")
    else:
        profile = request.user.profile
        user_lat = profile.latitude
        user_long = profile.longitude
        user_search_radius = profile.find_radius
        form = ProfileForm(label_suffix='', initial={'latitude': user_lat, 'longitude': user_long, 'search_radius': user_search_radius})
    return render(request, 'myprofile/profile.html', {
                            'form': form, 
                            'user_lat': user_lat, 
                            'user_long': user_long, 
                            'user_search_radius': user_search_radius})