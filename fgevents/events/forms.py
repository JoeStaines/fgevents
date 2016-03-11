from django.forms import ModelForm, Select

from .models import Events, WeeklyRecurringDate, MonthlyRecurringDate, OneTimeEventDate, EventGames

class EventForm(ModelForm):
    class Meta:
        model = Events
        fields = ['event_type','event_name',
                    'address','town','county','country','postcode',
                    'latitude','longitude',
                    'contact','info']
        widgets = { 'event_type': Select(attrs={'onChange': 'changeForm()'}) }
        
    def typechoices(self):
        return Events.EVENT_CHOICES
                    
class WeeklyDateForm(ModelForm):
    class Meta:
        model = WeeklyRecurringDate
        fields = ['weekday']
        
class MonthlyDateForm(ModelForm):
    class Meta:
        model = MonthlyRecurringDate
        fields = ['weekday', 'week_number']
        
class OneTimeDateForm(ModelForm):
    class Meta:
        model = OneTimeEventDate
        fields = ['start_date', 'end_date']
        
class EventGamesForm(ModelForm):
    class Meta:
        model = EventGames
        fields = ['game']