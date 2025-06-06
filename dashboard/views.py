from django.views import View
from django.shortcuts import render
from django.db.models import Sum
from indicators.models import Indicator
from logframe.models import Goal, Outcome, Output

class DashboardSummaryView(View):
    def get(self, request):
        # Count logframe items
        total_goals = Goal.objects.count()
        total_outcomes = Outcome.objects.count()
        total_outputs = Output.objects.count()
        total_indicators = Indicator.objects.count()

        indicators = Indicator.objects.all()

        # Progress computation helper
        def compute_progress(indicator):
            total_actual = indicator.indicatordata.aggregate(
                total=Sum('value')
            )['total'] or 0
            return round((total_actual / indicator.target) * 100, 2) if indicator.target else 0

        # Calculate progress for each indicator
        progress_values = [compute_progress(ind) for ind in indicators]

        # Average progress
        avg_progress = round(sum(progress_values) / len(progress_values), 2) if progress_values else 0

        # Latest indicators with progress
        latest_indicators = indicators.order_by('-id')[:5]
        progress_trends = [
            {
                "id": ind.id,
                "name": ind.name,
                "progress": compute_progress(ind),
            }
            for ind in latest_indicators
        ]

        context = {
            "totals": {
                "goals": total_goals,
                "outcomes": total_outcomes,
                "outputs": total_outputs,
                "indicators": total_indicators,
            },
            "average_progress": avg_progress,
            "progress_trends": progress_trends,
        }
        return render(request, "dashboard/dashboard.html", context)