from django.http import JsonResponse
from django.views import View
from indicators.models import Indicator
from logframe.models import Goal, Outcome, Output

class DashboardSummaryView(View):
    def get(self, request):
        total_goals = Goal.objects.count()
        total_outcomes = Outcome.objects.count()
        total_outputs = Output.objects.count()
        total_indicators = Indicator.objects.count()

        from django.db.models import Avg
        avg_progress = Indicator.objects.aggregate(avg_progress=Avg('progress')).get('avg_progress') or 0

        latest_indicators = Indicator.objects.order_by('-id')[:5]
        progress_trends = [
            {
                "id": ind.id,
                "name": ind.name,
                "progress": ind.progress,
            }
            for ind in latest_indicators
        ]

        data = {
            "totals": {
                "goals": total_goals,
                "outcomes": total_outcomes,
                "outputs": total_outputs,
                "indicators": total_indicators,
            },
            "average_progress": avg_progress,
            "progress_trends": progress_trends,
        }
        return JsonResponse(data)
