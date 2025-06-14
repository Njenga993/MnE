# dashboard/views.py

from django.views import View
from django.shortcuts import render
from django.db.models import Sum
from indicators.models import Indicator
from logframe.models import Goal, Outcome, Output


class DashboardSummaryView(View):
    def get(self, request):
        # Totals
        totals = {
            "goals": Goal.objects.count(),
            "outcomes": Outcome.objects.count(),
            "outputs": Output.objects.count(),
            "indicators": Indicator.objects.count(),
        }

        # Fetch all indicators with their related output and data
        indicators = Indicator.objects.select_related('output').prefetch_related('data')

        # Compute progress based on IndicatorData (sum of values)
        def compute_progress(indicator):
            total_actual = indicator.data.aggregate(
                total=Sum('value')
            )['total'] or 0

            target = indicator.target or 0
            if target == 0:
                return 0

            return round((total_actual / target) * 100, 2)

        # List of all progress values
        progress_values = []
        for ind in indicators:
            progress = compute_progress(ind)
            progress_values.append(progress)

        average_progress = round(sum(progress_values) / len(progress_values), 2) if progress_values else 0

        # 5 most recent indicators
        latest_indicators = indicators.order_by('-created_at')[:5]
        progress_trends = [
            {
                "id": ind.id,
                "name": ind.name,
                "progress": compute_progress(ind)
            }
            for ind in latest_indicators
        ]

        return render(request, "dashboard/dashboard.html", {
            "totals": totals,
            "average_progress": average_progress,
            "progress_trends": progress_trends,
        })
