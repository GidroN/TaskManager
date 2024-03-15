from django import forms
from django.utils import timezone
from .models import Task, Group


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'is_active', 'due_time', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'type': 'time'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].inital = timezone.localdate()


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
