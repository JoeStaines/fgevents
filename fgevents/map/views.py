from django.shortcuts import render

from events.models import Events

import datetime
# Create your views here.

def index(request):
    weekly_events = Events.objects.filter(event_type="week")
    monthly_events = Events.objects.filter(event_type="month")
    onetime_events = Events.objects.filter(onetime__end_date__gte=datetime.date.today())
    return render(request, 'map/map.html', {'weekly_events': weekly_events, 
                                                                 'monthly_events': monthly_events, 
                                                                 'onetime_events': onetime_events})
