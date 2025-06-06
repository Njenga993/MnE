#signals
# This file contains signal handlers for the indicators app.
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from indicators.models import Indicator
from logframe.models import Goal, Outcome, Output
@receiver(post_save, sender=Indicator)
def update_indicator(sender, instance, created, **kwargs):
    if created:
        print(f"Indicator created: {instance.name}")
    else:
        print(f"Indicator updated: {instance.name}")
@receiver(pre_delete, sender=Indicator)
def delete_indicator(sender, instance, **kwargs):
    print(f"Indicator deleted: {instance.name}")
@receiver(post_save, sender=Goal)
def update_goal(sender, instance, created, **kwargs):
    if created:
        print(f"Goal created: {instance.title}")
    else:
        print(f"Goal updated: {instance.title}")
@receiver(pre_delete, sender=Goal)
def delete_goal(sender, instance, **kwargs):
    print(f"Goal deleted: {instance.title}")
@receiver(post_save, sender=Outcome)
def update_outcome(sender, instance, created, **kwargs):
    if created:
        print(f"Outcome created: {instance.title}")
    else:
        print(f"Outcome updated: {instance.title}")
@receiver(pre_delete, sender=Outcome)
def delete_outcome(sender, instance, **kwargs):
    print(f"Outcome deleted: {instance.title}")
@receiver(post_save, sender=Output)
def update_output(sender, instance, created, **kwargs):
    if created:
        print(f"Output created: {instance.title}")
    else:
        print(f"Output updated: {instance.title}")
@receiver(pre_delete, sender=Output)
def delete_output(sender, instance, **kwargs):
    print(f"Output deleted: {instance.title}")
# This file contains signal handlers for the indicators app.