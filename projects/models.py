# projects/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('implementation', 'Implementation'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    donor = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_budget = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProjectMembership(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=[
        ('manager', 'Project Manager'),
        ('mne_officer', 'M&E Officer'),
        ('field_officer', 'Field Officer'),
        ('admin', 'Admin')
    ])

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Budget(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budgets')
    output = models.ForeignKey('logframe.Output', on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.CharField(max_length=255)
    amount_allocated = models.DecimalField(max_digits=12, decimal_places=2)
    amount_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.activity} - Allocated: {self.amount_allocated}"

    @property
    def remaining(self):
        return self.amount_allocated - self.amount_spent

    @property
    def spent_percentage(self):
        if self.amount_allocated > 0:
            return round((self.amount_spent / self.amount_allocated) * 100, 2)
        return 0
