# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["seats"]  # only user-editable field
        widgets = {
            "seats": forms.NumberInput(attrs={"min": 1, "class": "form-control"})
        }

    def clean_seats(self):
        seats = int(self.cleaned_data["seats"])
        if seats <= 0:
            raise forms.ValidationError("Seats must be at least 1.")
        return seats
