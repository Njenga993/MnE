from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'text', 'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'type': 'text', 'class': 'datepicker'}),
        }
