from django import forms
from .models import Project
from logframe.models import Goal, Outcome, Output, Indicator
from django.forms.models import inlineformset_factory

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'donor', 'start_date', 'end_date', 'total_budget']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Project Description'}),
            'donor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Donor'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total_budget': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Budget'})
        }

GoalFormSet = inlineformset_factory(Project, Goal, fields=['title', 'description'], extra=1, can_delete=True)
OutcomeFormSet = inlineformset_factory(Goal, Outcome, fields=['title', 'description'], extra=1, can_delete=True)
OutputFormSet = inlineformset_factory(Outcome, Output, fields=['title', 'description'], extra=1, can_delete=True)
IndicatorFormSet = inlineformset_factory(Output, Indicator, fields=['name', 'means_of_verification', 'unit_of_measurement', 'baseline', 'target', 'actual'], extra=1, can_delete=True)
from django.contrib.auth import get_user_model
User = get_user_model()
class UserSelectForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'class': 'form-control'})
class UserRoleForm(forms.Form):
    role = forms.ChoiceField(choices=[
        ('manager', 'Project Manager'),
        ('mne_officer', 'M&E Officer'),
        ('field_officer', 'Field Officer'),
        ('admin', 'Admin')
    ], label="Select Role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs.update({'class': 'form-control'})
class ProjectMembershipForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")
    role = forms.ChoiceField(choices=[
        ('manager', 'Project Manager'),
        ('mne_officer', 'M&E Officer'),
        ('field_officer', 'Field Officer'),
        ('admin', 'Admin')
    ], label="Select Role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].widget.attrs.update({'class': 'form-control'})
class ProjectSearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, label="Search Projects")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['query'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Search by project name or donor'})
from django import forms
from .models import Project, ProjectMembership
class ProjectMembershipForm(forms.ModelForm):
    class Meta:
        model = ProjectMembership
        fields = ['user', 'role']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.all()
        self.fields['role'].choices = [
            ('manager', 'Project Manager'),
            ('mne_officer', 'M&E Officer'),
            ('field_officer', 'Field Officer'),
            ('admin', 'Admin')
        ]
        self.fields['user'].label = "Select User"
        self.fields['role'].label = "Select Role"
class ProjectMembershipUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectMembership
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [
            ('manager', 'Project Manager'),
            ('mne_officer', 'M&E Officer'),
            ('field_officer', 'Field Officer'),
            ('admin', 'Admin')
        ]
        self.fields['role'].label = "Select Role"
class ProjectMembershipDeleteForm(forms.Form):
    confirm = forms.BooleanField(required=True, label="I confirm I want to remove this user from the project")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirm'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['confirm'].label = "Confirm Removal"
    def clean_confirm(self):
        confirm = self.cleaned_data.get('confirm')
        if not confirm:
            raise forms.ValidationError("You must confirm the removal of this user from the project.")
        return confirm