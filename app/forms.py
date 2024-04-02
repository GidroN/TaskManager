from django import forms
from django.contrib.auth.models import User

from .models import Task, Group
from .utils import FixedGroupsCalculator


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


class ExportJsonForm(forms.Form):
    def __init__(self, *args, user, **kwargs):
        super(ExportJsonForm, self).__init__(*args, **kwargs)
        self.fields['groups'].queryset = Group.objects.exclude(slug__in=FixedGroupsCalculator.FIXED_GROUPS).filter(user=user)

    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.none(), required=True,
                                            widget=forms.CheckboxSelectMultiple)


