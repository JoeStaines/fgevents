from django.forms import ModelForm, Select, Textarea, BaseFormSet
from django.forms.formsets import formset_factory
from django.core.exceptions import ValidationError

from .models import Events, WeeklyRecurringDate, MonthlyRecurringDate, OneTimeEventDate, EventGames

import datetime

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
        
class BaseMonthlyFormset(BaseFormSet):
    def clean(self):
        """ Check there is no combination of the same day and week """
        if any(self.errors):
            return
            
        days_week_pair = []
        for form in self.forms:
            day = form.cleaned_data['weekday']
            week_no = form.cleaned['week_number']
            pair = [day, week_no]
            if pair in days_week_pair:
                raise forms.ValidationError("The combination of week day and week number has to be unique")
            days.append(pair)
        
MonthlyDateFormset = formset_factory(MonthlyDateForm, formset=BaseMonthlyFormset, min_num=1, validate_min=True, extra=0, max_num=2)
        
class OneTimeDateForm(ModelForm):
    class Meta:
        model = OneTimeEventDate
        fields = ['start_date', 'end_date']
        
    def clean(self):
        if any(self.errors):
            return
    
        # Test the end date doesn't become before the start date
        cleaned_data = self.cleaned_data
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if end_date < start_date:
            raise ValidationError("The start date has to come before the end date")
            
        # Test start date not before current date
        today = datetime.date.today()
        if today > start_date:
            raise ValidationError("The date has to be today or in the future")
            

class BaseGamesFormset(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
            
        games = []
        for form in self.forms:
            game = form.cleaned_data['game']
            if game in games:
                raise ValidationError("Cannot list the same game twice")
            games.append(game)
            
class EventGamesForm(ModelForm):
    class Meta:
        model = EventGames
        fields = ['game']
        
EventGamesFormset = formset_factory(EventGamesForm, formset=BaseGamesFormset, min_num=1, validate_min=True, extra=0, max_num=15)