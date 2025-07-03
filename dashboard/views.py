from projects.models import Project
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count
from logframe.models import Indicator, Goal, Outcome, Output
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from projects.models import Budget
from activities.models import Activity
from django.http import HttpResponse



class DashboardSummaryView(View):
    def get(self, request):
        project_id = request.GET.get("project")
        selected_project = None

        # Defaults for when no project is selected
        goals = Goal.objects.none()
        outcomes = Outcome.objects.none()
        outputs = Output.objects.none()
        indicators = Indicator.objects.none()
        
        budget_items = []
        total_allocated = 0
        total_spent = 0

        if project_id:
            selected_project = get_object_or_404(Project, pk=project_id)

            goals = Goal.objects.filter(project=selected_project)
            outcomes = Outcome.objects.filter(goal__in=goals)
            outputs = Output.objects.filter(outcome__in=outcomes)
            indicators = Indicator.objects.filter(output__in=outputs)
            activities = Activity.objects.filter(project=selected_project)
            # Budget logic
            budget_items = selected_project.budgets.all()
            total_allocated = sum(b.amount_allocated for b in budget_items)
            total_spent = sum(b.amount_spent for b in budget_items)

        totals = {
            "goals": goals.count(),
            "outcomes": outcomes.count(),
            "outputs": outputs.count(),
            "indicators": indicators.count(),
        }

        # Comment count
        from comments.models import Comment
        from django.contrib.contenttypes.models import ContentType
        from django.db.models import Count, Sum

        indicator_ct = ContentType.objects.get_for_model(Indicator)
        comment_counts = Comment.objects.filter(
            content_type=indicator_ct,
            object_id__in=indicators.values_list('id', flat=True)
        ).values('object_id').annotate(count=Count('id'))

        comment_count_map = {item['object_id']: item['count'] for item in comment_counts}
        total_comments = sum(comment_count_map.values())

        def compute_progress(indicator):
            return indicator.progress_percentage()

        progress_values = []
        progress_trends = []

        for ind in indicators:
            progress = compute_progress(ind)
            progress_values.append(progress)
            progress_trends.append({
                "id": ind.id,
                "name": ind.name,
                "progress": progress,
                "output": ind.output.title if ind.output else "N/A",
                "goal": ind.output.outcome.goal.title if ind.output and ind.output.outcome and ind.output.outcome.goal else "N/A",
                "category": getattr(ind, 'category', 'Uncategorized'),
                "comment_count": comment_count_map.get(ind.id, 0)
            })

        average_progress = round(sum(progress_values) / len(progress_values), 2) if progress_values else 0

        # Top indicators chart
        top_indicators = sorted(progress_trends, key=lambda x: x['progress'], reverse=True)[:5]
        bar_labels = [ind['name'] for ind in top_indicators]
        bar_values = [ind['progress'] for ind in top_indicators]

        return render(request, "dashboard/dashboard.html", {
            "totals": totals,
            "average_progress": average_progress,
            "progress_trends": progress_trends,
            "categories": list(set(pt["category"] for pt in progress_trends)),
            "total_comments": total_comments,
            "bar_labels": bar_labels,
            "bar_values": bar_values,
            "projects": Project.objects.all(),
            "selected_project_id": project_id,
            "budget_items": budget_items,
            "total_allocated": total_allocated,
            "total_spent": total_spent,
            "activities": activities,

        })

