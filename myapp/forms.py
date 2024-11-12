# forms.py
from django import forms
from .models import Car
from .models import Booking
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'image', 'capacity', 'is_available', 'rent']
# bookings/forms.py
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date']
        
    widgets = {
        'booking_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select a date'}),
    }