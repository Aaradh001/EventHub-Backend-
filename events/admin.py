from django.contrib import admin
from .models import Event, EventCategory, Requirement
# Register your models here.
admin.site.register(Event)
admin.site.register(Requirement)
admin.site.register(EventCategory)
# admin.site.register(RequirementDetails)