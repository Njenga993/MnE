from django.db import models
from django.contrib.auth.models import User
from logframe.models import Output  # Make sure Output model is available

class IndicatorCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Indicator Categories"

    def __str__(self):
        return self.name


class Indicator(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(IndicatorCategory, on_delete=models.SET_NULL, null=True, related_name='indicators')
    output = models.ForeignKey(Output, on_delete=models.CASCADE, related_name='indicator_set_ind', null=True, blank=True)


    unit = models.CharField(max_length=50, null=True, blank=True)
    baseline = models.FloatField(default=0.0)
    target = models.FloatField()
    actual = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def progress(self):
        """Returns progress toward the target as a percentage"""
        if self.target > 0:
            return round((self.actual / self.target) * 100, 2)
        return 0


class IndicatorData(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='data')
    value = models.FloatField()
    date_collected = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_collected']

    def __str__(self):
        return f"{self.indicator.name} - {self.date_collected}"


class IndicatorActivity(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.name} ({self.indicator.name})"
