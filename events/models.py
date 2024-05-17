from django.db import models
from accounts.models import VendorProfile, ClientProfile
from services.models import Service
# from venue_management.models import Venue
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from jsonschema import validate
from typing import Optional
import datetime

# Create your models here.
class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cat_image = models.ImageField(upload_to='events/event-categories/', null = True, blank = True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'EventCategory'
        verbose_name_plural = 'Event Categories'
    
    def __str__(self):
        return self.name
    

class Event(models.Model):
    STATUS_CHOICES = (
        ('LAUNCHED', 'LAUNCHED'),
        ('PENDING', 'PENDING'),
        ('ASSIGNED', 'ASSIGNED'),
        ('WORK_IN_PROGRESS', 'WORK_IN_PROGRESS'),
        ('VERIFICATION_IN_PROGRESS', 'VERIFICATION_IN_PROGRESS'),
        ('COMPLETED', 'COMPLETED'),
    )
    event_id = models.CharField(max_length=150)
    event_cat = models.ForeignKey(EventCategory, on_delete=models.DO_NOTHING, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='events/eventthumb/', null = True, blank = True)
    # venue = models.ForeignKey(Venue, on_delete=models.DO_NOTHING)
    organiser = models.ForeignKey(VendorProfile, on_delete=models.DO_NOTHING, null=True, blank=True)
    client = models.ForeignKey(ClientProfile, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    guest_count = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_advance_paid = models.BooleanField(default=False)
    is_final_amount_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='LAUNCHED')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    # def save(self, *args, **kwargs):
    #     # Custom behavior before saving
    #     if not self.event_id:
    #         counter = Event.objects.all().count()+1
    #         self.event_id = 'EH'+str(round(datetime.datetime.now().timestamp()))+str(counter)

    #     # Call the original save method
    #     super(Event, self).save(*args, **kwargs)
    


# @deconstructible
# class BasicJsonValidator:
#     def __init__(self, types):
#         self.types = types

#     def __call__(self, mydict):
#         if not isinstance(mydict, dict):
#             raise ValidationError("Value must be a dictionary.")
#         for key, value in mydict.items():
#             if key not in self.types:
#                 raise ValidationError(f"key {key} should not be present")
#             if not isinstance(value, self.types[key]):
#                 raise ValidationError(
#                     f"for {key}, {value} should be a {self.types[key]}"
#                 )


class Requirement(models.Model):
    FOOD_PREFERENCE_CHOICES = [
    ('veg', 'Vegetarian'),
    ('non-veg', 'Non-Vegetarian'),
]
    CATERING_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "food_preferrence": {"type": "string", "enum": ["veg", "non-veg"]},
        "main_course": {"type": "array", "items": {"type": "string"} },
        "starters": {"type": "array", "items": {"type": "string"} },
        "desserts": {"type": "array", "items": {"type": "string"} },
        "welcome_drinks": {"type": "array", "items": {"type": "string"} },
        # Add more properties specific to instance 1
    },
    "required": ["food_preferrence", "main_course", "starters", "desserts", "welcome_drinks"]  # Specify required keys for instance 1
}
    DECORATION_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        # "theme_description": {"type": "string", "enum": ["veg", "non-veg"]},
        "theme_description": {"type": "string"},
        "size of the area": {"type": "number"},
        "layout_description": {"type": "string"},
        "props_and_materials": {"type": "array", "items": {"type": "string"}},
        "is_lighting_and effects_required": {"type": "boolean"},
        "lighting_and_effects": {"type": "array", "items": {"type": "string"}},
        "design_instructions": {"type": "string"},
        # Add more properties specific to instance 1
    },
    "required": []  # Specify required keys for instance 2
}


    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    req_name = models.CharField(max_length=150)
    has_sub = models.BooleanField(default=False)
    cost_per_unit = models.DecimalField(max_digits = 50, decimal_places = 2, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    start_time = models.DateField()
    requirement_details = models.JSONField(null=True)
    # parent = models.ForeignKey('self', null = True, blank = True, on_delete = models.CASCADE, related_name = 'children')

    def __str__(self):
        return self.req_name

    def save(self, *args, **kwargs):
        # Validate JSON data against the schema before saving
        if args and args.instance_type:
            if args.instance_type == 'CATERING':
                validate(instance=self.requirement_details, schema=self.CATERING_JSON_SCHEMA)
            elif args.instance_type == 'DECORATION':
                validate(instance=self.requirement_details, schema=self.DECORATION_JSON_SCHEMA)
        # validate(instance=self.json_data, schema=self.CATERING_JSON_SCHEMA)
        super().save(*args, **kwargs)
"""
For the child services, create sub services as planned by using the self relation. While creating requirements model,
create a flied for a csv file which will contain the updated service checkist. So based on the checklist uploaded by the client
the vendor can fix price for the particular service. 
"""

# class RequirementDetails(models.Model):

#     area_of_decoration_choices = (
#         ('STAGE', 'STAGE'),
#         ('HALL', 'HALL'),
#         ('BALL_ROOM', 'BALL_ROOM'),
#         ('COURTYARD', 'COURTYARD'),
#         ('ENTRANCE', 'ENTRANCE')
#         )
#     food_preferences = (
#         ('VEG', 'VEG'),
#         ('NON-VEG', 'NON-VEG')
#         )
#     requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, null=True, blank=True)
#     preferred_food = models.CharField(max_length=150, choices= food_preferences)
#     area_of_decoration = models.CharField(max_length=150, choices= area_of_decoration_choices, null=True, blank=True)
#     construction_needed = models.BooleanField(default=False)
#     checklist = models.FileField(upload_to="event/requirement_files/")

#     def __str__(self):
#         return self.requirement.req_name + "details"