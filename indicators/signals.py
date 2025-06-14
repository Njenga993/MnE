from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import Sum
from indicators.models import Indicator, IndicatorData
from logframe.models import Goal, Outcome, Output

# Log indicator creation/update
@receiver(post_save, sender=Indicator)
def log_indicator(sender, instance, created, **kwargs):
    print(f"Indicator {'created' if created else 'updated'}: {instance.name}")

# Log indicator deletion
@receiver(pre_delete, sender=Indicator)
def delete_indicator(sender, instance, **kwargs):
    print(f"Indicator deleted: {instance.name}")

# Auto-update actual when new data is added
@receiver(post_save, sender=IndicatorData)
def update_actual_on_data_save(sender, instance, **kwargs):
    indicator = instance.indicator
    total = indicator.indicatordata.aggregate(total=Sum('value'))['total'] or 0
    indicator.actual = total
    indicator.save()

# Log Goal/Outcome/Output activity
@receiver(post_save, sender=Goal)
def log_goal(sender, instance, created, **kwargs):
    print(f"Goal {'created' if created else 'updated'}: {instance.title}")

@receiver(pre_delete, sender=Goal)
def delete_goal(sender, instance, **kwargs):
    print(f"Goal deleted: {instance.title}")

@receiver(post_save, sender=Outcome)
def log_outcome(sender, instance, created, **kwargs):
    print(f"Outcome {'created' if created else 'updated'}: {instance.title}")

@receiver(pre_delete, sender=Outcome)
def delete_outcome(sender, instance, **kwargs):
    print(f"Outcome deleted: {instance.title}")

@receiver(post_save, sender=Output)
def log_output(sender, instance, created, **kwargs):
    print(f"Output {'created' if created else 'updated'}: {instance.title}")

@receiver(pre_delete, sender=Output)
def delete_output(sender, instance, **kwargs):
    print(f"Output deleted: {instance.title}")
