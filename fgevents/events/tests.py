from django.test import TestCase, Client
from django.core.exceptions import ValidationError

from .models import *

# Create your tests here.

def create_event(new_data={}):
    data = {
        'event_type': 'week',
        'event_name': 'Test',
        'latitude': 0.0,
        'longitude': 0.0,
        'contact': 'www.test.com',
        'info': 'Some test text',
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
        'month-0-week_number': 1
    }
    data.update(new_data)
    c = Client()
    c.post('/events/create/', data)
    
class EventCreateTests(TestCase):
    def test_event_saved(self):
        create_event()
        queryset = Events.objects.filter(event_name='Test')
        self.assertIsNotNone(queryset.first())
    
    def test_no_repeated_games(self):
        data = {
            'games-TOTAL_FORMS': 2,
            'games-1-game': 'Street Fighter 5'
        }
        self.assertRaises(ValidationError, create_event(data))
        
