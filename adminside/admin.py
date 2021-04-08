from django.contrib import admin
from .models import User, Agent, Clients, UserProfile


# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Agent)
admin.site.register(Clients)