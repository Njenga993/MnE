from django.contrib import admin
from .models import Indicator, IndicatorCategory, IndicatorData, IndicatorActivity


@admin.register(IndicatorCategory)
class IndicatorCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'target', 'updated_at']
    search_fields = ['name', 'description']
    list_filter = ['category']


@admin.register(IndicatorData)
class IndicatorDataAdmin(admin.ModelAdmin):
    list_display = ['indicator', 'value', 'date_collected', 'created_at']
    list_filter = ['indicator', 'date_collected', 'created_at']


@admin.register(IndicatorActivity)
class IndicatorActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'indicator', 'completed', 'timestamp']
    list_filter = ['indicator', 'user', 'action', 'timestamp']
