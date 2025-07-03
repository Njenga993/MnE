from django.shortcuts import render, get_object_or_404, redirect
from .models import Activity
from .forms import ActivityForm
from projects.models import Project

def activity_list(request):
    activities = Activity.objects.select_related('project', 'output')
    return render(request, 'activities/activity_list.html', {'activities': activities})

def activity_create(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('activity-list')
    else:
        form = ActivityForm()
    return render(request, 'activities/activity_form.html', {'form': form})

def activity_update(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activity-list')
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'activities/activity_form.html', {'form': form})

def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        activity.delete()
        return redirect('activity-list')
    return render(request, 'activities/activity_confirm_delete.html', {'activity': activity})
