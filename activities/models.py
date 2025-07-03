from django.db import models
from logframe.models import Output
from projects.models import Project

class Activity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activities')
    output = models.ForeignKey(Output, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    budget_allocated = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    budget_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='planned')

    def __str__(self):
        return f"{self.title} ({self.status})"

    @property
    def remaining(self):
        """
        Returns the remaining unspent budget.
        """
        return self.budget_allocated - self.budget_spent

    @property
    def percent_spent(self):
        """
        Returns the percentage of the allocated budget that has been spent.
        """
        if self.budget_allocated > 0:
            return round((self.budget_spent / self.budget_allocated) * 100, 2)
        return 0
