from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from .forms import *
from .models import Events

# Create your views here.

def index(request):
    events = Events.objects.all()
    return render(request, 'events/eventlist.html', {'events': events})

def detail(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    return render(request, 'events/detail.html', {'event': event})
    
@login_required    
def createevent(request):
    # Apply prefixes to the forms so the field names do not clash
    # e.g., there is a 'weekday' field both in the weekly form and monthly form
    # and one will overwrite the other
    event_form = EventForm(prefix="event", label_suffix='')
    
    weekly_formset = WeeklyDateFormset(prefix="week")
    monthly_formset = MonthlyDateFormset(prefix="month")
    games_formset = EventGamesFormset(prefix="games")
    onetime_form = OneTimeDateForm(prefix="onetime")

    if request.method == "POST":
        valid = True
        event_form = EventForm(request.POST, prefix="event", label_suffix='')
        weekly_formset = WeeklyDateFormset(request.POST, prefix="week")
        monthly_formset = MonthlyDateFormset(request.POST, prefix="month")
        onetime_form = OneTimeDateForm(request.POST, prefix="onetime", label_suffix='')
        games_formset = EventGamesFormset(request.POST, prefix="games")
        
        if event_form.is_valid():
            event_type = event_form.cleaned_data["event_type"]
            
            if not games_formset.is_valid():
                valid = False
        
            if event_type == "week":
                if not weekly_formset.is_valid():
                    valid = False
            if event_type == "month":
                if not monthly_formset.is_valid():
                    valid = False
            if event_type == "onetime":
                if not onetime_form.is_valid():
                    valid = False
        
        
        
        
            if valid:
                event = event_form.save(commit=False)
                event.userID = request.user
                event.save()
                
                # Save games
                for games_form in games_formset:
                    games_obj = games_form.save(commit=False)
                    games_obj.eventID = event
                    games_obj.save()
                
                # Save form depending on the type
                if event_type == "week":
                    for week_form in weekly_formset:
                        week_obj = week_form.save(commit=False)
                        week_obj.eventID = event
                        week_obj.save()
                               
                elif event_type == "month":
                    for month_form in monthly_formset:
                        month_obj = month_form.save(commit=False)
                        month_obj.eventID = event
                        month_obj.save()
                                           
                elif event_type == "onetime":
                    onetime_obj = onetime_form.save(commit=False)
                    onetime_obj.eventID = event
                    onetime_obj.save()
                
                return redirect(reverse("eventfeed-index"))
            
    return render(request, 'events/createevent.html', {
                'event_form': event_form,
                'weekly_formset': weekly_formset,
                'monthly_formset': monthly_formset,
                'games_formset': games_formset,
                'onetime_form': onetime_form
                })
                