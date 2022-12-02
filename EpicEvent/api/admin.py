from django.contrib import admin
from .models import Client, Contrat, EventStatus, Event

# Register your models here.
admin.site.register(Client)
admin.site.register(Contrat)
admin.site.register(EventStatus)
admin.site.register(Event)