from django.shortcuts import render, redirect

from .forms import *

# Create your views here.

def index(request):
    pass
    
def createevent(request):
    # Apply prefixes to the forms so the field names do not clash
    # e.g., there is a 'weekday' field both in the weekly form and monthly form
    # and one will overwrite the other
    event_form = EventForm(prefix="event", label_suffix='')
    
    weekly_formset = WeeklyDateFormset(prefix="week", label_suffix='')
    monthly_formset = MonthlyDateFormset(prefix="month", label_suffix='')
    games_formset = EventGamesFormset(prefix="games", label_suffix='')

    if request.method == "POST":
        event_form = EventForm(request.POST, prefix="event", label_suffix='')
        if event_form.is_valid():
            event_type = event_form.cleaned_data['event_type']
            # Validate and save form depending on the type
            if event_type == "week":
                week_form = WeeklyDateForm(request.POST, prefix="week", label_suffix='')
                print week_form.is_valid()
                if week_form.is_valid():
                    print "in wekk event"
                    event = event_form.save()
                    date_obj = week_form.save(commit=False)
            elif event_type == "month":
                month_form = MonthlyDateForm(request.POST, prefix="month", label_suffix='')
                if month_form.is_valid():
                    event = event_form.save()
                    date_obj = month_form.save(commit=False)
            elif event_type == "onetime":
                onetime_form = OneTimeDateForm(request.POST, prefix="onetime", label_suffix='')
                if onetime_form.is_valid():
                    event = event_form.save()
                    date_obj = onetime_form.save(commit=False)
            
            # After validating the forms, apply the event to the foreign key of the date obja nd save
            date_obj.eventID = event
            date_obj.save()
            return redirect("/")
        
    return render(request, 'events/createevent.html', {
                'event_form': event_form,
                'week_form': week_form,
                'month_form': month_form,
                'onetime_form': onetime_form,
                'weekly_formset': weekly_formset,
                'monthly_formset': monthly_formset,
                'games_formset': games_formset
                })
                