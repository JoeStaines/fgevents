from django.forms import ModelForm, Select, Textarea, BaseFormSet
from django.forms.formsets import formset_factory

from .models import Events, WeeklyRecurringDate, MonthlyRecurringDate, OneTimeEventDate, EventGames

class EventForm(ModelForm):
    class Meta:
        model = Events
        fields = ['event_type','event_name',
                    'latitude','longitude',
                    'contact','info']
        widgets = { 'event_type': Select(attrs={'onChange': 'changeForm()'}),
                          'info': Textarea(attrs={'placeholder': 'Address information, event rules, directions or any other information about the event'})}
        
    def typechoices(self):
        return Events.EVENT_CHOICES
                    
class WeeklyDateForm(ModelForm):
    class Meta:
        model = WeeklyRecurringDate
        fields = ['weekday']

class BaseWeeklyFormset(BaseFormSet):
    def clean(self):
        """ Check no two days are the same """
        if any(self.errors):
            return
            
        days = []
        for form in self.forms:
            day = form.cleaned_data['weekday']
            if day in days:
                raise forms.ValidationError("Days have to be unique")
            days.append(day)
        
WeeklyDateFormset = formset_factory(WeeklyDateForm, formset=BaseWeeklyFormset, min_num=1, validate_min=True, extra=0, max_num=2)
        
class MonthlyDateForm(ModelForm):
    class Meta:
        model = MonthlyRecurringDate
        fields = ['weekday', 'week_number']
        
MonthlyDateFormset = formset_factory(MonthlyDateForm, min_num=1, validate_min=True, extra=0, max_num=2)
        
class OneTimeDateForm(ModelForm):
    class Meta:
        model = OneTimeEventDate
        fields = ['start_date', 'end_date']
        
class EventGamesForm(ModelForm):
    class Meta:
        model = EventGames
        fields = ['game']
        
EventGamesFormset = formset_factory(EventGamesForm, min_num=1, validate_min=True, extra=0, max_num=15)