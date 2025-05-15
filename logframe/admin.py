# admin.py for logframe
from django.contrib import admin
from .models import Goal, Outcome, Output, Indicator

admin.site.register(Goal)
admin.site.register(Outcome)
admin.site.register(Output)
admin.site.register(Indicator)
