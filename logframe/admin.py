from django.contrib import admin
from .models import Goal, Outcome, Output, Indicator


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'created_at')
    list_filter = ('project',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)


@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal', 'project')
    list_filter = ('goal__project',)
    search_fields = ('title', 'description')

    def project(self, obj):
        return obj.goal.project


@admin.register(Output)
class OutputAdmin(admin.ModelAdmin):
    list_display = ('title', 'outcome', 'project')
    list_filter = ('outcome__goal__project',)
    search_fields = ('title', 'description')

    def project(self, obj):
        return obj.outcome.goal.project


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'output', 'project', 'target', 'actual')
    list_filter = ('output__outcome__goal__project',)
    search_fields = ('name', 'means_of_verification')

    def project(self, obj):
        return obj.output.outcome.goal.project
