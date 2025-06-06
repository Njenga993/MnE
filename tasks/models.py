from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
class TaskComment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.task.title}'
class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='task_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Attachment for {self.task.title} by {self.uploaded_at}'
class TaskHistory(models.Model):
    task = models.ForeignKey(Task, related_name='history', on_delete=models.CASCADE)
    action = models.CharField(max_length=255)  # e.g., 'created', 'updated', 'deleted'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'History for {self.task.title} by {self.user.username} at {self.timestamp}'
class TaskLabel(models.Model):
    task = models.ForeignKey(Task, related_name='labels', on_delete=models.CASCADE)
    label = models.CharField(max_length=50)

    def __str__(self):
        return f'Label "{self.label}" for {self.task.title}'
class TaskPriority(models.Model):
    task = models.ForeignKey(Task, related_name='priority', on_delete=models.CASCADE)
    priority_level = models.CharField(max_length=50)  # e.g., 'Low', 'Medium', 'High'

    def __str__(self):
        return f'Priority "{self.priority_level}" for {self.task.title}'
class TaskStatus(models.Model):
    task = models.ForeignKey(Task, related_name='status', on_delete=models.CASCADE)
    status = models.CharField(max_length=50)  # e.g., 'Open', 'In Progress', 'Closed'

    def __str__(self):
        return f'Status "{self.status}" for {self.task.title}'
class TaskReminder(models.Model):
    task = models.ForeignKey(Task, related_name='reminders', on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()  # When to send the reminder
    notified = models.BooleanField(default=False)  # Whether the reminder has been sent

    def __str__(self):
        return f'Reminder for {self.task.title} at {self.reminder_time}'
    