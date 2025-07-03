from django.db import models
from projects.models import Project

class Goal(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Outcome(models.Model):
    goal = models.ForeignKey(Goal, related_name='outcomes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    @property
    def project(self):
        return self.goal.project


class Output(models.Model):
    outcome = models.ForeignKey(Outcome, related_name='outputs', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    @property
    def project(self):
        return self.outcome.goal.project


class Indicator(models.Model):
    output = models.ForeignKey(Output, related_name='indicators', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    means_of_verification = models.TextField()
    unit_of_measurement = models.CharField(max_length=100, blank=True)
    baseline = models.FloatField(default=0)
    target = models.FloatField(default=0)
    actual = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def progress_percentage(self):
        if self.target > 0:
            return round((self.actual / self.target) * 100, 2)
        return 0

    @property
    def project(self):
        return self.output.outcome.goal.project
