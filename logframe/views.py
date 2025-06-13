# views.py for logframe
from rest_framework import viewsets
from django.http import HttpResponse
from .models import Goal, Outcome, Output, Indicator
from .serializers import GoalSerializer, OutcomeSerializer, OutputSerializer, IndicatorSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms

def goals_view(request):
    return render(request, 'logframe/goals.html')

class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['title', 'description', 'goal']

def outcomes_view(request):
    outcomes = Outcome.objects.select_related('goal').all()
    form = OutcomeForm()

    if request.method == 'POST':
        form = OutcomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('outcomes-ui')

    return render(request, 'logframe/outcomes.html', {
        'outcomes': outcomes,
        'form': form
    })


def outputs_view(request):
    outputs = Output.objects.select_related('outcome').all()
    outcomes = Outcome.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        outcome_id = request.POST.get('outcome')

        if title and description and outcome_id:
            try:
                outcome = Outcome.objects.get(id=outcome_id)
                Output.objects.create(title=title, description=description, outcome=outcome)
                return redirect('outputs')
            except Outcome.DoesNotExist:
                pass  # handle error if needed

    return render(request, 'logframe/outputs.html', {
        'outputs': outputs,
        'outcomes': outcomes
    })


def indicators_view(request):
    indicators = Indicator.objects.all()
    outputs = Output.objects.all()

    return render(request, 'logframe/indicators.html', {
        'indicators': indicators,
        'outputs': outputs
    })

@login_required
def logframe_home_view(request):
    return render(request, "logframe/logframe_home.html")


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

