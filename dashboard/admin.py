from django.contrib import admin
from .models import Dashboard, Widget, DashboardWidget


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'widget_type', 'position']
    search_fields = ['name']
    list_filter = ['widget_type']


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['dashboard', 'widget', 'order']
    list_filter = ['dashboard']
