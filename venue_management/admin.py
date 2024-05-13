from django.contrib import admin
from .models import Venue, Amenities, VenueImage
# Register your models here.
admin.site.register(Venue)
admin.site.register(Amenities)
admin.site.register(VenueImage)