from django.test import TestCase, Client
from django.core.exceptions import ValidationError

from .models import *
from myauth.models import MyUser

import datetime

# Create your tests here.

def create_event(new_data={}, c=Client()):
    data = {
        'event-event_type': 'week',
        'event-event_name': 'Test',
        'event-latitude': 0.0,
        'event-longitude': 0.0,
        'event-contact': 'www.test.com',
        'event-info': 'Some test text',
        'games-TOTAL_FORMS': 1,
        'games-INITIAL_FORMS': 0,
        'games-MAX_NUM_FORMS': 15,
        'games-0-game': 'Street Fighter 5',
        'week-TOTAL_FORMS': 1,
        'week-INITIAL_FORMS': 0,
        'week-MAX_NUM_FORMS': 2,
        'week-0-weekday': 0,
        'month-TOTAL_FORMS': 1,
        'month-INITIAL_FORMS': 0,
        'month-MAX_NUM_FORMS': 2,
        'month-0-weekday': 0,
        'month-0-week_number': 1,
    }
    data.update(new_data)
    return c.post('/events/create/', data)

def date_to_string(date):
    return "{}-{}-{}".format(date.year, date.month, date.day)

class EventCreateTests(TestCase):
    def setUp(self):
        user = MyUser.objects.create_user('temp@temp.com', 'temporary')
        self.c = Client()
        self.c.login(email="temp@temp.com", password="temporary")

    def test_event_saved(self):
        create_event(c=self.c)
        queryset = Events.objects.filter(event_name='Test')
        self.assertIsNotNone(queryset.first())
    
    def test_no_repeated_games(self):
        data = {
            'games-TOTAL_FORMS': 2,
            'games-1-game': 'Street Fighter 5'
        }
        response = create_event(data, self.c)
        self.assertFormsetError(response, "games_formset",  None, None, "Cannot list the same game twice", "")
        
    def test_start_date_before_end_date(self):
        today = datetime.date.today()
        start_date = today + datetime.timedelta(days=1)
        end_date = today + datetime.timedelta(days=2)
        start_str = date_to_string(start_date)
        end_str = date_to_string(end_date)
        data = {
            'event-event_type': 'onetime',
            'onetime-start_date': start_str,
            'onetime-end_date': end_str
        }
        create_event(data, self.c)
        queryset = Events.objects.filter(event_name='Test')
        self.assertIsNotNone(queryset.first())
        queryset = OneTimeEventDate.objects.filter(start_date__contains=start_date)
        self.assertIsNotNone(queryset.first())
        
    def test_date_after_end_date(self):
        today = datetime.date.today()
        start_date = today + datetime.timedelta(days=2)
        end_date = today + datetime.timedelta(days=1)
        start_str = date_to_string(start_date)
        end_str = date_to_string(end_date)
        data = {
            'event-event_type': 'onetime',
            'onetime-start_date': start_str,
            'onetime-end_date': end_str
        }
        response = create_event(data, self.c)
        self.assertFormError(response, "onetime_form",  None, "The start date has to come before the end date", "")
        
    def test_start_date_before_today(self):
        today = datetime.date.today()
        start_date = today + datetime.timedelta(days=-1)
        end_date = today + datetime.timedelta(days=1)
        start_str = date_to_string(start_date)
        end_str = date_to_string(end_date)
        data = {
            'event-event_type': 'onetime',
            'onetime-start_date': start_str,
            'onetime-end_date': end_str
        }
        response = create_event(data, self.c)
        self.assertFormError(response, "onetime_form",  None, "The date has to be today or in the future", "")
        
