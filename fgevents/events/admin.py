from django.contrib import admin

from .models import *
# Register your models here.

class WeeklyDateInline(admin.TabularInline):
    model = WeeklyRecurringDate
    
class MonthlyDateInline(admin.TabularInline):
    model = MonthlyRecurringDate
    
class OneTimeDateInline(admin.TabularInline):
    model = OneTimeEventDate

class EventsAdmin(admin.ModelAdmin):
    inlines = (WeeklyDateInline,MonthlyDateInline,OneTimeDateInline)
    
admin.site.register(Events, EventsAdmin)