from django.db import models
from django.utils.text import slugify

class Service(models.Model):

    unit_of_measurement_choices = (
        ('Persons Count','Persons Count'),
        ('Count', 'Count'),
        ('Area(Sq_Ft)', 'Area(Sq_Ft)')
    )
    TYPE_CHOICES = [
        ('CATERING', 'CATERING'),
        ('DECORATION', 'DECORATION'),
        ('OTHERS', 'OTHERS')
    ]
    name = models.CharField(max_length = 100)
    slug = models.SlugField(unique = True, null = True, blank = True)
    # cost_per_unit = models.DecimalField(max_digits = 50, decimal_places = 2)
    thumbnail = models.ImageField(upload_to="service/thumbnail", null=True, blank=True)
    service_type = models.CharField(max_length=150, choices=TYPE_CHOICES, null=True, blank=True)   
    unit_of_measurement = models.CharField(max_length = 100, choices=unit_of_measurement_choices, default='PERSON_COUNT')
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        print("kjeghfjksdgbfjkgeufgjkegfukdhsbgkj")
        if not self.slug:
            self.slug = slugify(self.name)
        super(Service, self).save(*args, **kwargs)
 
    def __str__(self):
        return self.name