from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.

WEEKDAYS = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)

class Events(models.Model):
    EVENT_CHOICES = ( 
        ( 'week', 'Weekly'),
        ( 'month', 'Monthly'),
        ( 'onetime', 'One Time Event') )
    event_type = models.CharField(max_length=10, choices=EVENT_CHOICES, default='week')
    event_name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    contact = models.CharField(max_length=100)
    info = models.TextField(max_length=20000)
    date_created = models.DateTimeField(auto_now_add=True)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL)
    
class WeeklyRecurringDate(models.Model):
    eventID = models.ForeignKey(Events)
    weekday = models.CharField(max_length=1, choices=WEEKDAYS)
    
class MonthlyRecurringDate(models.Model):
    eventID = models.ForeignKey(Events)
    weekday = models.CharField(max_length=1, choices=WEEKDAYS)
    
    WEEK_NUMBERS = (
        (1, "1st Week"),
        (2, "2nd Week"),
        (3, "3rd Week"),
        (4, "4th Week")
    )
    
    week_number = models.CharField(max_length=1, choices=WEEK_NUMBERS)
    
class OneTimeEventDate(models.Model):
    eventID = models.OneToOneField(Events, on_delete=models.CASCADE, primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
class EventGames(models.Model):
    eventID = models.ForeignKey(Events)
    game = models.CharField(max_length=50)