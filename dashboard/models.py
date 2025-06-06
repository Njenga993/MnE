from django.db import models


class Dashboard(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Widget(models.Model):
    
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=50)
    position = models.IntegerField()
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')

    def __str__(self):
        return self.name


class DashboardWidget(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='dashboard_widgets')
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.dashboard.title} - {self.widget.name}"
