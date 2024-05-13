from django.contrib import admin
from .models import Account, ClientProfile, VendorProfile, OtherServices

# Register your models here.
admin.site.register(Account)
admin.site.register(ClientProfile)
admin.site.register(VendorProfile)
admin.site.register(OtherServices)