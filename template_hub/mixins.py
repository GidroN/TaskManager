from django.http import HttpResponseForbidden

from .models import Template


class UserAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        template_id = self.kwargs.get('template_id')

        try:
            template = Template.objects.get(id=template_id, user=user)
        except Template.DoesNotExist:
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)
