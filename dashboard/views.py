# dashboard/views.py
from django.views import View
from django.shortcuts import render
from django.db.models import Sum, Count
from indicators.models import Indicator
from logframe.models import Goal, Outcome, Output
from comments.models import Comment  # ADD THIS
from django.contrib.contenttypes.models import ContentType


class DashboardSummaryView(View):
    def get(self, request):
        # Totals
        totals = {
            "goals": Goal.objects.count(),
            "outcomes": Outcome.objects.count(),
            "outputs": Output.objects.count(),
            "indicators": Indicator.objects.count(),
        }

        # --- Comment Counts ---
        indicator_ct = ContentType.objects.get_for_model(Indicator)
        total_comments = Comment.objects.filter(content_type=indicator_ct).count()

        # Get comment counts per indicator in a dictionary: {object_id: count}
        comment_counts = Comment.objects.filter(content_type=indicator_ct)\
            .values('object_id').annotate(count=Count('id'))
        comment_count_map = {item['object_id']: item['count'] for item in comment_counts}

        # Fetch all indicators with related output/outcome/goal
        indicators = Indicator.objects.select_related(
            'output__outcome__goal'
        ).prefetch_related('data')

        def compute_progress(indicator):
            total_actual = indicator.data.aggregate(
                total=Sum('value')
            )['total'] or 0

            target = indicator.target or 0
            if target == 0:
                return 0

            return round((total_actual / target) * 100, 2)

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
                "comment_count": comment_count_map.get(ind.id, 0)  # ADD THIS
            })

        average_progress = round(sum(progress_values) / len(progress_values), 2) if progress_values else 0

        return render(request, "dashboard/dashboard.html", {
            "totals": totals,
            "average_progress": average_progress,
            "progress_trends": progress_trends,
            "categories": list(set([pt['category'] for pt in progress_trends])),
            "total_comments": total_comments,  # ADD THIS
        })
