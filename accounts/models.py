from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from location_field.models.plain import PlainLocationField
from services.models import Service
from django.utils.text import slugify


class MyAccountManager(BaseUserManager):

    def create(self, username, email, user_role, phone_number = None, password = None):
        if not email:
            raise ValueError("Email address is mandatory")
        # if not password:
        #     raise ValueError("password is mandatory")
            
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            user_role = user_role,
            phone_number = phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, phone_number, email, password = None):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
            user_role = 'ADMIN',
            phone_number = phone_number
        )
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user
            

class Account(AbstractBaseUser):
    ROLE_CHOICES = (
        ("CLIENT", "CLIENT"),
        ("VENDOR", "VENDOR"),
        ("ADMIN", "ADMIN")
        )
    REG_CHOICES = (
        ("GOOGLE", "GOOGLE"),
        ("NORMAL", "NORMAL")
        )
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    registration_method = models.CharField(max_length = 100, choices = REG_CHOICES, default = 'NORMAL')
    user_role = models.CharField(max_length = 100, choices = ROLE_CHOICES)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'username', 'phone_number']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    def full_name(self):
        return {self.username} 
    
    def has_perm(self, perm, obj = None):
        return self.is_superadmin
    
    def has_module_perms(self, add_label):
        return True
    

class ClientProfile(models.Model):
    client = models.OneToOneField(Account, on_delete = models.CASCADE, related_name = 'client_profile')
    first_name = models.CharField(max_length = 100)
    last_name  = models.CharField(max_length = 100)
    profile_pic = models.ImageField(upload_to='client/profile_pic/', null = True, blank= True)
    area_of_preference = PlainLocationField(based_fields=['city'], zoom=9)
    
    def __str__(self):
        return self.first_name + self.last_name

    
    
    
    
class AddressBook(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50,blank=True,null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if self.is_default:
            # Set is_default=False for other addresses of the same user
            AddressBook.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super(AddressBook, self).save(*args, **kwargs)
        
    def get_user_full_address(self):
        address_parts = [self.name, self.phone,self.address_line_1]

        if self.address_line_2:
            address_parts.append(self.address_line_2)
        
        address_parts.append(f'<b>Pin: {self.pincode}</b>')
        address_parts.extend([self.city, self.state, self.country])
        
        
        return ', '.join(address_parts)
        # return f'{self.name},{self.phone},Pin:{self.pincode},Address:{self.address_line_1},{self.address_line_2},{self.city},{self.state},{self.country}'
    def __str__(self):
        return self.name
    

class VendorProfile(models.Model):
    extreme_low = 'LESS THAN 1L'
    low = '1L-10L'
    medium = '10L -25L'
    high = 'GREATER THAN 25L'

    SERVICE_CAPACITY_CHOICES = (
        (extreme_low, extreme_low),
        (low, low),
        (medium, medium),
        (high, high)
    )
    vendor = models.OneToOneField(Account, on_delete = models.CASCADE, related_name = 'vendor_profile')
    company_name = models.CharField(max_length = 100)
    logo = models.ImageField(upload_to = 'vendor/logo/', null = True, blank = True)
    website = models.CharField(max_length = 100)
    service_capacity = models.CharField(max_length = 100, choices = SERVICE_CAPACITY_CHOICES)
    is_verification_completed = models.BooleanField(default = False)
    specialised_on = models.ManyToManyField(Service, related_name = 'services_specialised_on')

    def __str__(self):
        return self.company_name
    

class OtherServices(models.Model):
    unit_of_measurement_choices = (
        ('OTHER_UNIT', 'OTHER_UNIT'),
        ('PERSON_COUNT', 'PERSON_COUNT'),
        ('COUNT', 'COUNT'),
        ('AREA(Sq_Ft)', 'AREA(Sq_Ft)')
    )
    name = models.CharField(max_length = 100)
    thumbnail = models.ImageField(upload_to="service/thumbnail", null=True, blank=True)
    is_active = models.BooleanField(default = True)

    # parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='childservice')
    cost_per_unit = models.DecimalField(max_digits = 50, decimal_places = 2, null=True, blank=True)
    unit_of_measurement = models.CharField(max_length = 100, choices=unit_of_measurement_choices, default='PERSON_COUNT')
    vendor = models.ForeignKey(VendorProfile, on_delete = models.CASCADE)
    other_unit_of_measurement = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return "Additional Service :" + self.name
    
    def save(self, *args, **kwargs):
        if self.other_unit_of_measurement:
            self.unit_of_measurement = "OTHER_UNIT"
            
        super(OtherServices, self).save(*args, **kwargs)