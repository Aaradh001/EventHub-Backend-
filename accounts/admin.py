from django.contrib import admin
from .models import Account, ClientProfile

# Register your models here.
admin.site.register(Account)
admin.site.register(ClientProfile)