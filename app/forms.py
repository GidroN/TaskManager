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


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class ExportJSONForm(forms.Form):
    def __init__(self, *args, user, **kwargs):
        super(ExportJSONForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['groups'].queryset = Group.objects.filter(user=user)
            self.fields['tasks'].queryset = Task.objects.filter(group__user=user)

    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.none(), required=False,
                                            widget=forms.CheckboxSelectMultiple)
    tasks = forms.ModelMultipleChoiceField(queryset=Task.objects.none(), required=False,
                                           widget=forms.CheckboxSelectMultiple)
