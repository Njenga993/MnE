from django.contrib import admin
from .models import Indicator, IndicatorCategory, IndicatorData, IndicatorActivity


@admin.register(IndicatorCategory)
class IndicatorCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


class IndicatorDataInline(admin.TabularInline):
    model = IndicatorData
    extra = 1
    readonly_fields = ['created_at']


class IndicatorActivityInline(admin.TabularInline):
    model = IndicatorActivity
    extra = 1
    readonly_fields = ['timestamp']


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'output', 'baseline', 'target', 'actual', 'unit', 'updated_at']
    search_fields = ['name', 'description', 'unit']
    list_filter = ['category', 'output']
    date_hierarchy = 'updated_at'
    ordering = ['-updated_at']
    inlines = [IndicatorDataInline, IndicatorActivityInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'output')
        }),
        ('Measurement Details', {
            'fields': ('unit', 'baseline', 'target', 'actual')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']


@admin.register(IndicatorData)
class IndicatorDataAdmin(admin.ModelAdmin):
    list_display = ['indicator', 'value', 'date_collected', 'created_at']
    list_filter = ['indicator', 'date_collected']
    search_fields = ['indicator__name']
    date_hierarchy = 'date_collected'
    ordering = ['-date_collected']


@admin.register(IndicatorActivity)
class IndicatorActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'indicator', 'user', 'action', 'completed', 'timestamp']
    list_filter = ['indicator', 'user', 'action', 'completed']
    search_fields = ['name', 'indicator__name', 'user__username']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
