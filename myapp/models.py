from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('dealer', 'Dealer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='customer')

class Car(models.Model):
    # Other fields for the Car model
    model = models.CharField(max_length=100)
    image = models.ImageField(upload_to="")
    # ForeignKey to represent the one-to-many relationship with CustomUser
    car_dealer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,  # This specifies what happens when the referenced CustomUser is deleted
        related_name='cars',       # This allows you to access the related cars from a CustomUser instance
    )
    capacity = models.CharField(max_length=2)
    is_available = models.BooleanField(default=True)
    rent = models.CharField(max_length=10, blank=True)
    def __str__(self):
        return f"{self.model}"
class Booking(models.Model):
    status_choices = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.car} "