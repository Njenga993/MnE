from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'output', 'start_date', 'end_date', 'budget_allocated', 'budget_spent', 'remaining', 'status')
    list_filter = ('project', 'status')
    search_fields = ('title',)
