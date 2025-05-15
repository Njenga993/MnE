# models.py for indicators

# indicators/models.py

from django.db import models

class Indicator(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    baseline = models.FloatField(default=0)
    target = models.FloatField(default=1)  # Avoid zero target to prevent division errors
    unit_of_measure = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # New field for progress %
    progress = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if self.target and self.target != 0:
            self.progress = (self.baseline / self.target) * 100
            # Clamp progress between 0 and 100
            if self.progress < 0:
                self.progress = 0
            elif self.progress > 100:
                self.progress = 100
        else:
            self.progress = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

