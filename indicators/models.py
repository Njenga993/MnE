from django.db import models
from django.contrib.auth.models import User


class IndicatorCategory(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Indicator(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(IndicatorCategory, on_delete=models.SET_NULL, null=True)
    target = models.FloatField()
    unit = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class IndicatorData(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    value = models.FloatField()
    date_collected = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.indicator.name} - {self.date_collected}"


class IndicatorActivity(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.indicator.name})"
