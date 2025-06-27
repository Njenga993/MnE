from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, ProjectMembership, Budget
from logframe.models import Goal, Outcome, Output, Indicator
from django.db.models import Sum
from django.http import JsonResponse
from .forms import ProjectForm, GoalFormSet

def project_create_with_logframe(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        goal_formset = GoalFormSet(request.POST)

        if project_form.is_valid() and goal_formset.is_valid():
            project = project_form.save(commit=False)
            project.created_by = request.user
            project.save()
            goal_formset.instance = project
            goal_formset.save()
            return redirect('project-detail', pk=project.pk)

    else:
        project_form = ProjectForm()
        goal_formset = GoalFormSet()

    return render(request, 'projects/project_create_with_logframe.html', {
        'project_form': project_form,
        'goal_formset': goal_formset,
    })

# === Project List ===
class ProjectListView(LoginRequiredMixin, View):
    def get(self, request):
        user_projects = Project.objects.filter(memberships__user=request.user)
        return render(request, 'projects/project_list.html', {'projects': user_projects})


# === Project Detail with Logframe Summary ===
class ProjectDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)

        # Optional: ensure user is a member
        if not ProjectMembership.objects.filter(user=request.user, project=project).exists():
            return render(request, '403.html', status=403)

        goals = project.goals.prefetch_related('outcomes__outputs__indicators')
        budgets = project.budgets.select_related('output')

        total_spent = budgets.aggregate(total=Sum('amount_spent'))['total'] or 0
        total_allocated = budgets.aggregate(total=Sum('amount_allocated'))['total'] or 0

        return render(request, 'projects/project_detail.html', {
            'project': project,
            'goals': goals,
            'budgets': budgets,
            'total_spent': total_spent,
            'total_allocated': total_allocated,
        })


# === Project Create/Edit ===
class ProjectCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProjectForm()
        return render(request, 'projects/project_form.html', {'form': form})

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            ProjectMembership.objects.create(project=project, user=request.user, role='manager')
            return redirect('project-detail', pk=project.pk)
        return render(request, 'projects/project_form.html', {'form': form})


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(instance=project)
        return render(request, 'projects/project_form.html', {'form': form, 'edit': True})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project-detail', pk=project.pk)
        return render(request, 'projects/project_form.html', {'form': form, 'edit': True})

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return project.created_by == self.request.user


# === Project Delete ===
class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        return render(request, 'projects/project_confirm_delete.html', {'project': project})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return redirect('project-list')

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return project.created_by == self.request.user
