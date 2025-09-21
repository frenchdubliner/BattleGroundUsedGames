from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Game(models.Model):
    CONDITION_CHOICES = [
        ('new in shrink', 'New in Shrink - Original shrinkwrap/seal is intact. Never Opened'),
        ('like new', 'Like New - Pieces unpunched, cards wrapped, never played'),
        ('very good', 'Very Good - Pieces punched, Sorted. Rarely or never played. No discernible wear'),
        ('good', 'Good - Played but well maintained. Pieces unsorted. Box/book(s) shows signs of use'),
        ('fair', 'Fair - Discernible wear. Box/book(s) shows minor damage and/or have been slightly marked'),
        ('poor', 'Poor - Worn but playable. Box/book(s) shows damage and/or have been significantly marked'),
    ]

    PET_CHOICES = [
        ('none', 'None'),
        ('cat', 'Cat'),
        ('dog', 'Dog'),
    ]
    
    name = models.CharField(max_length=200, help_text='Enter the name of the game')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games', help_text='User who owns this game')
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        help_text='Price of the game (minimum $0.01)'
    )
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default='good',
        help_text='Select the condition of the game'
    )
    missing_pieces = models.BooleanField(
        default=False,
        help_text='Check if the game has missing pieces'
    )
    description_of_missing_pieces = models.TextField(
        null=True,
        blank=True,
        help_text='Describe what pieces are missing (e.g., "Missing 2 red dice and instruction manual")'
    )
    smoking_house = models.BooleanField(
        default=False,
        help_text='Check if the game has been exposed to smoke from a smoking household'
    )
    musty_smell = models.BooleanField(
        default=False,
        help_text='Check if the game has a musty or unpleasant odor'
    )
    pet = models.CharField(
        max_length=10,
        choices=PET_CHOICES,
        default='none',
        help_text='Select if the game has been exposed to pets'
    )
    printed = models.BooleanField(
        default=False,
        help_text='Check if the game is a printed/custom version'
    )
    received = models.BooleanField(
        default=False,
        help_text='Check if the game has been received by the store (admin only)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
    
    def __str__(self):
        return f"{self.name} - {self.get_condition_display()} - ${self.price}"
    
    @property
    def formatted_price(self):
        """Return formatted price with currency symbol"""
        return f"${self.price}"
    
    def is_printed_visible_to_user(self, user):
        """Check if the printed field should be visible to the given user"""
        return user.is_authenticated and user.is_staff
    
    @property
    def admin_only_printed_status(self):
        """Return printed status only for admin users"""
        return str(self.printed)
    
    def is_received_visible_to_user(self, user):
        """Check if the received field should be visible to the given user"""
        return user.is_authenticated and user.is_staff
    
    @property
    def admin_only_received_status(self):
        """Return received status only for admin users"""
        return str(self.received)
