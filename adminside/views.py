from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django .contrib import messages
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetDoneView
)
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from .models import Agent, User, Clients, UserProfile
from .forms import (
    ClientModelForm,
    AgentModelForm,
    AssignAgentForm,
    CustomUserCreationForm,
    ClientForm
)
from .mixins import (
    OrganisorAndLoginRequiredMixin,
    OrganisorAndAgentAndLoginRequiredMixin
)


# Create your views here.
class AdminPasswordChangeView(OrganisorAndAgentAndLoginRequiredMixin, PasswordChangeView):
    template_name = 'adminside/password-change.html'
    success_url = reverse_lazy('adminside:password-change-done-view')


class AdminPasswordResetDoneView(OrganisorAndAgentAndLoginRequiredMixin, PasswordResetDoneView):
    template_name = 'adminside/password-reset-done.html'


class HomePageView(OrganisorAndAgentAndLoginRequiredMixin, generic.TemplateView):
    template_name = "adminside/home.html"


# def home(request):
#     return render(request, "adminside/home.html")


def index(request):
    return render(request, "adminside/create.html")


class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "adminside/agent_list.html"
    context_object_name = "agents"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


# def agent_list(request):
#     agents = Agent.objects.all()
#     context = {
#         "agents": agents
#     }
#     return render(request, "adminside/agent_client_list.html", context)


class AgentDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "adminside/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


# def agent_detail(request, pk):
#     agent = Agent.objects.get(id=pk)
#     context = {
#         "agent": agent
#     }
#     return render(request, "adminside/agent_detail.html", context)


class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "adminside/agent_create.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("adminside:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_client = False
        user.is_agent = True
        user.is_organisor = False
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        # agent.organisation = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView, self).form_valid(form)


# def agent_create(request):
#     form = AgentModelForm()
#     if request.method == "POST":
#         form = AgentModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("/agents")
#     context = {
#         "form": form
#     }
#     return render(request, "adminside/agent_create.html", context)


class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "adminside/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("adminside:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


# def agent_update(request, pk):
#     agent = Agent.objects.get(id=pk)
#     form = AgentModelForm(instance=agent)
#     if request.method == "POST":
#         form = AgentModelForm(request.POST, instance=agent)
#         if form.is_valid():
#             form.save()
#             return redirect("/agents")
#     context = {
#         "form": form,
#         "agent": agent
#     }
#     return render(request, "adminside/agent_update.html", context)


class AgentDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "adminside/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("adminside:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


# def agent_delete(request, pk):
#     agent = Agent.objects.get(id=pk)
#     agent.delete()
#     return redirect("/agents")


class ClientListView(OrganisorAndAgentAndLoginRequiredMixin, generic.ListView):
    template_name = "adminside/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        user = self.request.user

        # initial queryset of clients for the entire organisation
        if user.is_organisor:
            queryset = Clients.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False
            )
        else:
            queryset = Clients.objects.filter(
                organisation=user.agent.organisation,
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Clients.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                "organisor_clients": queryset
            })
        return context


# def client_list(request):
#     clients = Clients.objects.all()
#     context = {
#         "clients": clients
#     }
#     return render(request, "adminside/client_list.html", context)


class ClientDetailView(OrganisorAndAgentAndLoginRequiredMixin, generic.DetailView):
    template_name = "adminside/client_detail.html"
    context_object_name = "client"

    def get_queryset(self):
        user = self.request.user

        # initial queryset of clients for the entire organisation
        if user.is_organisor:
            queryset = Clients.objects.filter(organisation=user.userprofile)
        else:
            queryset = Clients.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


# def client_detail(request, pk):
#     client = Clients.objects.get(id=pk)
#     context = {
#         "client": client
#     }
#     return render(request, "adminside/client_detail.html", context)


class AgentClientListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "adminside/agent_client_list.html"
    context_object_name = "agents"

    def get_context_data(self, **kwargs):
        context = super(AgentClientListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Clients.objects.filter(
                organisation=user.userprofile
            )

        context.update({
            "organisor_clients_count": queryset.filter(agent__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Agent.objects.filter(
                organisation=user.userprofile
            )
        return queryset


class AgentAndClientDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "adminside/agent_client_detail.html"
    context_object_name = "agentclient"

    # def get_context_data(self, **kwargs):
    #     context = super(AgentAndClientDetailView, self).get_context_data(**kwargs)
    #     clients = self.get_object().clients.all()
    #     context.update({
    #         "clients": clients
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Agent.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Agent.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class ClientCreateView(OrganisorAndAgentAndLoginRequiredMixin, generic.CreateView):
    template_name = "adminside/client_create.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("adminside:client-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_client = True
        user.is_agent = False
        user.is_organisor = False
        user.save()
        a = self.request.user.userprofile
        if self.request.user.is_organisor:
            Clients.objects.create(
                user=user,
                # agent=Agent.objects.get(user__username=a),
                organisation=self.request.user.userprofile
            )
        elif self.request.user.is_agent:
            Clients.objects.create(
                user=user,
                agent=Agent.objects.get(user__username=a),
                organisation=UserProfile.objects.get(user__username="rock")
            )
        return super(ClientCreateView, self).form_valid(form)


# def client_create(request):
#     form = ClientModelForm()
#     if request.method == "POST":
#         form = ClientModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("/adminside/clients")
#     context = {
#         "form": form
#     }
#     return render(request, "adminside/client_create.html", context)


class ClientUpdateView(OrganisorAndAgentAndLoginRequiredMixin, generic.UpdateView):
    template_name = "adminside/client_update.html"
    form_class = ClientModelForm
    context_object_name = "client"

    def get_success_url(self):
        return reverse("adminside:client-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of clients for the entire organisation
        return Clients.objects.filter(organisation=user.userprofile)


# class ClientAddBal(OrganisorAndAgentAndLoginRequiredMixin, generic.UpdateView):
#     template_name = "adminside/client_add_bal.html"
#     form_class = ClientForm
#     context_object_name = "client"
#
#     def get_success_url(self):
#         return reverse("adminside:client-list")

    # def form_valid(self, form):
    #     user = form.save(commit=False)
    #     user.is_client = True
    #     user.is_agent = False
    #     user.is_organisor = False
    #     user.save()
#
#     def get_queryset(self):
#         user = self.request.user
#         # initial queryset of clients for the entire organisation
#         return Clients.objects.filter(organisation=user.userprofile)


def client_add_bal(request, pk):
    if request.user.is_authenticated and (request.user.is_agent or request.user.is_organisor):
        client = Clients.objects.get(id=pk)
        agent = client.agent
        form = ClientForm()
        if request.method == "POST":
            form = ClientForm(request.POST)
            if form.is_valid():
                bal = form.cleaned_data['bal']
                if bal > agent.bal:
                    messages.error(request, "You can't add bal, please add sufficient balance first")
                    return HttpResponseRedirect(reverse('adminside:client-add-bal', args=(client.pk,)))
                else:
                    agent.bal = agent.bal - bal
                    agent.save()
                    client.bal = client.bal + bal
                    client.save()
                    return HttpResponseRedirect(reverse('adminside:client-detail', args=(client.pk,)))
    context = {
        "form": form,
        "client": client
    }
    return render(request, "adminside/client_add_bal.html", context)


# def client_update(request, pk):
#     client = Clients.objects.get(id=pk)
#     form = ClientModelForm(instance=client)
#     if request.method == "POST":
#         form = ClientModelForm(request.POST, instance=client)
#         if form.is_valid():
#             form.save()
#             return redirect("/clients")
#     context = {
#         "form": form,
#         "client": client
#     }
#     return render(request, "adminside/client_update.html", context)


class ClientDeleteView(OrganisorAndAgentAndLoginRequiredMixin, generic.DeleteView):
    template_name = "adminside/client_delete.html"

    def get_success_url(self):
        return reverse("adminside:client-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of clients for the entire organisation
        return Clients.objects.filter(organisation=user.userprofile)


# def client_delete(request, pk):
#     client = Clients.objects.get(id=pk)
#     client.delete()
#     return redirect("/clients")


class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "adminside/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("adminside:client-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        client = Clients.objects.get(id=self.kwargs["pk"])
        client.agent = agent
        client.save()
        return super(AssignAgentView, self).form_valid(form)