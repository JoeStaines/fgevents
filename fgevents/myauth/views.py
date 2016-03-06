from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout

from myauth.admin import UserCreationForm
from .forms import LoginForm

# Create your views here.
# Font: Russo
def log_in(request):

    # Redirect user if they are already logged in
    if request.user.is_authenticated():
        return redirect("/")

    error_message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    error_message = "User not active"
            else:
                error_message = "User does not exist with this username and password"
    else:
        form = LoginForm()
    return render(request, "myauth/login.html", {'form': form, 'error_message': error_message})
    
def log_out(request):
    logout(request)
    return redirect(reverse("login"))
    
def register(request):
    
    # Redirect user if they are already logged in
    if request.user.is_authenticated():
        return redirect("/")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            if not request.POST.get('findplayers', False):
                profile = new_user.profile
                profile.find_radius = 0
                profile.save()
            return redirect(reverse("profile-index"))
    else:
        form = UserCreationForm()
    return render(request, "myauth/register.html", {'form': form})