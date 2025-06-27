from projects.models import Project
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count
from indicators.models import Indicator
from logframe.models import Goal, Outcome, Output
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType


class DashboardSummaryView(View):
    def get(self, request):
        project_id = request.GET.get("project")
        selected_project = None

        if project_id:
            selected_project = get_object_or_404(Project, pk=project_id)

        # If a project is selected, fetch data for that project
        if selected_project:
            goals = Goal.objects.filter(project=selected_project)
            outcomes = Outcome.objects.filter(goal__in=goals)
            outputs = Output.objects.filter(outcome__in=outcomes)
            indicators = Indicator.objects.filter(output__in=outputs).select_related(
                'output__outcome__goal'
            ).prefetch_related('data')
        else:
            # Return nothing if no project is selected
            goals = Goal.objects.none()
            outcomes = Outcome.objects.none()
            outputs = Output.objects.none()
            indicators = Indicator.objects.none()

        # Count totals
        totals = {
            "goals": goals.count(),
            "outcomes": outcomes.count(),
            "outputs": outputs.count(),
            "indicators": indicators.count(),
        }

        # Comment count map
        indicator_ct = ContentType.objects.get_for_model(Indicator)
        comment_counts = Comment.objects.filter(
            content_type=indicator_ct,
            object_id__in=indicators.values_list('id', flat=True)
        ).values('object_id').annotate(count=Count('id'))

        comment_count_map = {item['object_id']: item['count'] for item in comment_counts}
        total_comments = sum(comment_count_map.values())

        # Compute progress
        def compute_progress(indicator):
            total_actual = indicator.data.aggregate(total=Sum('value'))['total'] or 0
            target = indicator.target or 0
            return round((total_actual / target) * 100, 2) if target else 0

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

        # (Optional) Top indicators for chart
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
            "selected_project_id": project_id
        })
