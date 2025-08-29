# core/models.py
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string


def generate_booking_id() -> str:
    return get_random_string(12).upper()


class TravelOption(models.Model):
    # Must match your DB columns exactly (see DESCRIBE core_traveloption)
    travel_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=10)
    source = models.CharField(max_length=120)
    destination = models.CharField(max_length=120)
    departure_at = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()  # column: available_seats

    class Meta:
        ordering = ["departure_at"]

    def __str__(self) -> str:
        return f"{self.travel_id} {self.source}→{self.destination} @ {self.departure_at:%Y-%m-%d %H:%M}"

    # Convenience alias so templates and code can use .seats consistently
    @property
    def seats(self) -> int:
        return int(self.available_seats)

    @seats.setter
    def seats(self, value: int) -> None:
        self.available_seats = int(value)


class Booking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    booking_id = models.CharField(
        max_length=24, unique=True, default=generate_booking_id, editable=False
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings", db_index=True
    )
    travel_option = models.ForeignKey(
        TravelOption, on_delete=models.CASCADE, related_name="bookings"
    )
    seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.CONFIRMED
    )
    booked_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["booked_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.booking_id} ({self.user.username})"

    @classmethod
    def create_booking(cls, user: User, travel_option: TravelOption, seats: int):
        seats = int(seats)
        if seats <= 0:
            raise ValidationError("Seats must be at least 1.")

        available = int(travel_option.seats)
        if seats > available:
            raise ValidationError(f"Only {available} seat(s) left.")

        total = (travel_option.price or Decimal("0")) * Decimal(seats)

        booking = cls.objects.create(
            user=user,
            travel_option=travel_option,
            seats=seats,
            total_price=total,
            status=cls.Status.CONFIRMED,
        )

        # decrement seats on the trip
        travel_option.seats = available - seats
        travel_option.save(update_fields=["available_seats"])

        return booking

    def can_cancel(self) -> bool:
        return (
            self.status == Booking.Status.CONFIRMED
            and self.travel_option.departure_at > timezone.now()
        )
