from rest_framework import viewsets
from django.http import HttpResponse
from .models import Goal, Outcome, Output, Indicator
from .serializers import GoalSerializer, OutcomeSerializer, OutputSerializer, IndicatorSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from projects.models import Project

# ---------------- API ViewSets -------------------
class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer

class OutputViewSet(viewsets.ModelViewSet):
    queryset = Output.objects.all()
    serializer_class = OutputSerializer

class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer

# ---------------- GOALS -------------------
def goals_view(request):
    project_id = request.GET.get('project')
    if not project_id or not project_id.isdigit():
        return redirect('logframe-home')

    project = get_object_or_404(Project, pk=int(project_id))

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title:
            Goal.objects.create(title=title, description=description, project=project)
            print(f"✅ Created goal for project: {project.id} - {project.name}")
            return redirect(f'{request.path}?project={project_id}')
        else:
            return HttpResponse("⚠️ Title is required.", status=400)

    goals = Goal.objects.filter(project=project)

    return render(request, 'logframe/goals.html', {
        'goals': goals,
        'project': project
    })

# ---------------- OUTCOMES -------------------
class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['title', 'description', 'goal']

def outcomes_view(request):
    project_id = request.GET.get('project')
    if not project_id or not project_id.isdigit():
        return redirect('logframe-home')

    project = get_object_or_404(Project, pk=int(project_id))
    goals = Goal.objects.filter(project=project)
    outcomes = Outcome.objects.filter(goal__in=goals)

    form = OutcomeForm()
    form.fields['goal'].queryset = goals

    if request.method == 'POST':
        form = OutcomeForm(request.POST)
        form.fields['goal'].queryset = goals
        if form.is_valid():
            outcome = form.save(commit=False)
            if outcome.goal.project != project:
                return HttpResponse("⚠️ Invalid goal selection for this project.", status=400)
            outcome.save()
            print(f"✅ Created outcome linked to goal: {outcome.goal} and project: {project.name}")
            return redirect(f'{request.path}?project={project_id}')

    return render(request, 'logframe/outcomes.html', {
        'outcomes': outcomes,
        'form': form,
        'project': project,
    })

# ---------------- OUTPUTS -------------------
def outputs_view(request):
    project_id = request.GET.get('project')
    if not project_id or not project_id.isdigit():
        return redirect('logframe-home')

    project = get_object_or_404(Project, pk=int(project_id))
    outcomes = Outcome.objects.filter(goal__project=project)
    outputs = Output.objects.filter(outcome__in=outcomes)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        outcome_id = request.POST.get('outcome')

        if title and description and outcome_id:
            try:
                outcome = Outcome.objects.get(id=outcome_id, goal__project=project)
                Output.objects.create(title=title, description=description, outcome=outcome)
                print(f"✅ Created output under outcome: {outcome.title} for project: {project.name}")
                return redirect(f'{request.path}?project={project_id}')
            except Outcome.DoesNotExist:
                print("❌ Outcome not found or doesn't belong to this project.")
                return HttpResponse("Invalid outcome for this project", status=400)
        else:
            return HttpResponse("⚠️ All fields are required.", status=400)

    return render(request, 'logframe/outputs.html', {
        'outputs': outputs,
        'outcomes': outcomes,
        'project': project,
    })

# ---------------- INDICATORS -------------------
def indicators_view(request):
    project_id = request.GET.get('project')
    if not project_id or not project_id.isdigit():
        return redirect('logframe-home')

    project = get_object_or_404(Project, pk=int(project_id))
    outputs = Output.objects.filter(outcome__goal__project=project)
    indicators = Indicator.objects.filter(output__in=outputs)

    if request.method == 'POST':
        name = request.POST.get('name')
        means = request.POST.get('means_of_verification')
        unit = request.POST.get('unit_of_measurement', '')
        baseline = request.POST.get('baseline', 0)
        target = request.POST.get('target', 0)
        actual = request.POST.get('actual', 0)
        output_id = request.POST.get('output')

        try:
            output = Output.objects.get(id=output_id, outcome__goal__project=project)
            Indicator.objects.create(
                name=name,
                means_of_verification=means,
                unit_of_measurement=unit,
                baseline=baseline,
                target=target,
                actual=actual,
                output=output
            )
            print(f"✅ Created indicator under output: {output.title} for project: {project.name}")
            return redirect(f'{request.path}?project={project_id}')
        except Output.DoesNotExist:
            print("❌ Output not found or doesn't belong to this project.")
            return HttpResponse("Invalid output for this project", status=400)

    return render(request, 'logframe/indicators.html', {
        'indicators': indicators,
        'outputs': outputs,
        'project': project,
    })

# ---------------- LOGFRAME HOME -------------------
@login_required
def logframe_home_view(request):
    projects = Project.objects.all()
    selected_project_id = request.GET.get('project')
    return render(request, "logframe/logframe_home.html", {
        'projects': projects,
        'selected_project_id': selected_project_id,
    })
