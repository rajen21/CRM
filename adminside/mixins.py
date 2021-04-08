from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django .contrib import messages


class OrganisorAndLoginRequiredMixin(AccessMixin):
    """verify that the current user is authenticated and is an organisor."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organisor:
            return redirect("adminside:client-list")
        return super().dispatch(request, *args, **kwargs)


class OrganisorAndAgentAndLoginRequiredMixin(AccessMixin):
    """verify that the current user is authenticated and is an agent."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or (not request.user.is_agent and not request.user.is_organisor):
            messages.error(request, 'Access denied')
            return redirect("adminside:login")
        return super().dispatch(request, *args, **kwargs)