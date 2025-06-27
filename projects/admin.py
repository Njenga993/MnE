from django.contrib import admin
from .models import Project, ProjectMembership, Budget
from logframe.models import Goal, Outcome, Output, Indicator


# === Inline Admins for Logframe ===

class IndicatorInline(admin.TabularInline):
    model = Indicator
    extra = 0
    fields = ('name', 'means_of_verification', 'unit_of_measurement', 'baseline', 'target', 'actual')
    readonly_fields = ('progress_percentage',)

class OutputInline(admin.TabularInline):
    model = Output
    extra = 0
    fields = ('title', 'description')
    show_change_link = True

class OutcomeInline(admin.TabularInline):
    model = Outcome
    extra = 0
    fields = ('title', 'description')
    show_change_link = True

class GoalInline(admin.TabularInline):
    model = Goal
    extra = 0
    fields = ('title', 'description')
    show_change_link = True


# === Main Project Admin ===

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'donor', 'start_date', 'end_date', 'total_budget', 'created_by')
    search_fields = ('name', 'donor')
    list_filter = ('start_date', 'end_date')
    readonly_fields = ('created_at',)
    inlines = [GoalInline]  # Only show top-level here

@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'role')
    list_filter = ('role', 'project')
    search_fields = ('user__username',)

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('project', 'output', 'activity', 'amount_allocated', 'amount_spent')
    search_fields = ('activity',)
    list_filter = ('project',)
    readonly_fields = ('remaining', 'spent_percentage')
# === Logframe Admins ===
