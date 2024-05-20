from django.db import models



class Amenities(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


# Create your models here.
class Venue(models.Model):
    VENUE_TYPE_CHOICES = (
        ('OUTDOOR', 'OUTDOOR'),
        ('INDOOR', 'INDOOR'),
        ('RESORT', 'RESORT'),
        ('AUDITORIUM', 'AUDITORIUM')
    )
    
    RESERVATION_CHOICES = (
        ('AVAILABLE', 'AVAILABLE'),
        ('BOOKED', 'BOOKED'),
        ('UNAVAILABLE', 'UNAVAILABLE'),
    )

    name = models.CharField(max_length=300, db_index=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    management_company = models.CharField(max_length=150, null=True, blank=True)
    rental_fees = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    reservation_status = models.CharField(max_length=150, choices=RESERVATION_CHOICES, db_index=True, default='AVAILABLE')
    full_address = models.TextField(default="", null=True, blank=True)
    add_line_1 = models.TextField()
    add_line_2 = models.TextField(default="", null=True, blank=True)
    lat_long = models.CharField(max_length=200, null=True, blank=True)
    street = models.CharField(max_length=300, null=True, blank=True, db_index=True, default="")
    city = models.CharField(max_length=150, db_index=True)
    state = models.CharField(max_length=200, db_index=True)
    country = models.CharField(max_length=200, db_index=True)
    thumbnail = models.ImageField(upload_to='venue/thumbnail', null=True, blank=True)
    pincode = models.IntegerField(db_index=True)
    description = models.TextField(null=True, blank=True)
    venue_type = models.CharField(max_length=150, choices=VENUE_TYPE_CHOICES, db_index=True)
    amenities = models.ManyToManyField(Amenities, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ', ' + self.city + ', ' + self.state
    
    def get_venue_address(self):
        address_parts = [self.name, self.add_line_1, self.add_line_2, self.street]
        address_parts.append(f'Pin: {self.pincode}')
        address_parts.extend([self.city, self.state, self.country])
        return ', '.join(address_parts)

    def save(self, *args, **kwargs):
        self.full_address = self.get_venue_address()
        super(Venue, self).save(*args, **kwargs)


class VenueImage(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='venue_images/')
    caption = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.caption} ({self.venue.name})"