from django.urls import path, include
from . import views
from django.contrib.auth.views import (
    LoginView,
    LogoutView
)

app_name = "adminside"

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('create/', views.index),
    path('agent/<int:pk>/', views.AgentDetailView.as_view(), name='agent-detail'),
    path('client/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('client/<int:pk>/addbal', views.client_add_bal, name='client-add-bal'),
    path('client/<int:pk>/cupdate/', views.ClientUpdateView.as_view(), name='client-update'),
    path('agent/<int:pk>/aupdate/', views.AgentUpdateView.as_view(), name='agent-update'),
    path('client/<int:pk>/cdel/', views.ClientDeleteView.as_view(), name='client-delete'),
    path('agent/<int:pk>/adel/', views.AgentDeleteView.as_view(), name='agent-delete'),
    path('<int:pk>/assign-agent/', views.AssignAgentView.as_view(), name='assign-agent'),
    path('clientcreate/', views.ClientCreateView.as_view(), name='client-create'),
    path('agentcreate/', views.AgentCreateView.as_view(), name='agent-create'),
    path('clients/', views.ClientListView.as_view(), name='client-list'),
    path('agents/', views.AgentListView.as_view(), name='agent-list'),
    path('agentsclients/', views.AgentClientListView.as_view(), name='agent-clients-list'),
    path('agentsclients/<int:pk>/', views.AgentAndClientDetailView.as_view(), name='agent-clients'),
    path('admin-change-password/', views.AdminPasswordChangeView.as_view(), name='password-change-view'),
    path('admin-change-password/done/', views.AdminPasswordResetDoneView.as_view(), name='password-change-done-view'),
    path('login/', LoginView.as_view(template_name="adminside/login.html"), name='login'),
    path('logout/', LogoutView.as_view(next_page="adminside:login"), name='logout'),
]