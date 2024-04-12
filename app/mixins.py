from django.http import HttpResponseForbidden
from django.views.generic.base import ContextMixin

from app.models import Group, Task
from app.utils import get_groups_context_data


class GroupsDataMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_context = get_groups_context_data(self.request.user)
        context.update(group_context)
        return context


class UserAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        group_slug = self.kwargs.get('group_slug')
        task_id = self.kwargs.get('pk')

        try:
            group = Group.objects.get(slug=group_slug, user=user)
        except Group.DoesNotExist:
            return HttpResponseForbidden()

        if task_id:
            try:
                Task.objects.get(id=task_id, group=group)
            except Task.DoesNotExist:
                return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)
