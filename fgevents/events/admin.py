from django.contrib import admin

from .models import *
# Register your models here.

class WeeklyDateInline(admin.TabularInline):
    model = WeeklyRecurringDate

class EventsAdmin(admin.ModelAdmin):
    inlines = (WeeklyDateInline,)
    
admin.site.register(Events, EventsAdmin)