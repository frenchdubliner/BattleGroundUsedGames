from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Create your models here.
class Profile(models.Model):
    DROPOFF_LOCATION_CHOICES = [
        ('Abington', 'Abington'),
        ('Norton', 'Norton'),
        ('Saugus', 'Saugus'),
        ('Framingham', 'Framingham'),
    ]
    
    PAYMENT_CHOICE_CHOICES = [
        ('cash_40', '40% of sale value in cash'),
        ('credit_70', '70% of sale value in store credit'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    display_name = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, help_text='Enter phone number (e.g., +1-555-123-4567)')
    dropoff_location = models.CharField(
        max_length=20,
        choices=DROPOFF_LOCATION_CHOICES,
        default='Abington',
        help_text='Select your preferred dropoff location'
    )
    payment_choice = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICE_CHOICES,
        default='credit_70',
        help_text='Select your preferred payment method'
    )
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
    @property
    def name(self):
        if self.display_name:
            name = self.display_name
        else:
            name = self.user.username
        return name
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar.svg')
        return avatar