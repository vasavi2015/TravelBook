# core/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import TravelOption, Booking
from django.contrib import admin

admin.site.site_header = "TRAVELBOOK Admin"
admin.site.site_title = "TRAVELBOOK Admin"
admin.site.index_title = "Dashboard"
class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = ("booking_id", "travel_option", "seats", "total_price", "status", "booked_at")
    readonly_fields = ("booking_id", "total_price", "booked_at")
    ordering = ("-booked_at",)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_id", "user", "travel_option", "seats", "total_price", "status", "booked_at")
    list_filter = ("status", "travel_option__type")
    search_fields = (
        "booking_id", "user__username", "user__email",
        "travel_option__travel_id", "travel_option__source", "travel_option__destination",
    )
    autocomplete_fields = ("user", "travel_option")
    readonly_fields = ("booking_id", "booked_at")
    ordering = ("-booked_at",)

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ("travel_id", "type", "source", "destination", "departure_at", "price", "available_seats")
    search_fields = ("travel_id", "source", "destination")
    list_filter = ("type",)
    ordering = ("-departure_at",)

# Optional: show a user’s bookings right on the User admin page
User = get_user_model()
try:
    admin.site.unregister(User)  # ok if it was already registered
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [BookingInline]
