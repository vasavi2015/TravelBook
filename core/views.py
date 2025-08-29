from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView, DetailView

from .forms import RegisterForm, ProfileForm, BookingForm
from .models import TravelOption, Booking



def home(request):
    return render(request, "core/home.html")


def logout_now(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("travel_list")
        # Optional: surface errors via messages too
        messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "core/register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)  # edit built-in User
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "core/profile.html", {"form": form})



class TravelListView(ListView):
    model = TravelOption
    template_name = "core/travel_list.html"
    context_object_name = "travels"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            TravelOption.objects.filter(departure_at__gte=timezone.now())
            .order_by("departure_at")
        )
        q = self.request.GET.get("q")
        t = self.request.GET.get("type")
        src = self.request.GET.get("source")
        dst = self.request.GET.get("destination")
        date = self.request.GET.get("date")

        if q:
            qs = qs.filter(
                Q(source__icontains=q)
                | Q(destination__icontains=q)
                | Q(travel_id__icontains=q)
            )
        if t:
            qs = qs.filter(type=t)
        if src:
            qs = qs.filter(source__icontains=src)
        if dst:
            qs = qs.filter(destination__icontains=dst)
        if date:
            qs = qs.filter(departure_at__date=date)
        return qs


class TravelDetailView(DetailView):
    model = TravelOption
    template_name = "core/travel_detail.html"
    context_object_name = "travel"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = BookingForm()
        return ctx


@login_required
def create_booking(request, pk):
    travel = get_object_or_404(TravelOption, pk=pk)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                seats = form.cleaned_data["seats"]
                booking = Booking.create_booking(
                    user=request.user,
                    travel_option=travel,   # ✅ pass the object, not travel_option_id
                    seats=seats,
                )
                messages.success(
                    request, f"Booking {booking.booking_id} confirmed!"
                )
                return redirect("booking_list")
            except ValidationError as e:
                messages.error(request, e.messages[0])
    else:
        form = BookingForm()
    return render(request, "core/booking_form.html", {"form": form, "travel": travel})


class BookingListView(ListView):
    model = Booking
    template_name = "core/booking_list.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return (
            Booking.objects
            .filter(user=self.request.user)
            .select_related("travel_option")
            .order_by("-booked_at")                 # 👈 newest first
        )

# core/views.py
@login_required
def cancel_booking(request, pk):
    if request.method != "POST":
        return redirect("booking_list")

    booking = get_object_or_404(
        Booking.objects.select_related("travel_option"),
        pk=pk,
        user=request.user,
    )

    if not booking.can_cancel():
        messages.warning(request, "This booking cannot be cancelled.")
        return redirect("booking_list")

    # mark cancelled
    booking.status = Booking.Status.CANCELLED
    booking.save(update_fields=["status"])

    # release seats back to the trip (use the REAL column)
    trip = booking.travel_option
    trip.available_seats = trip.available_seats + booking.seats
    trip.save(update_fields=["available_seats"])   # or just trip.save()

    messages.success(request, f"Booking {booking.booking_id} cancelled.")
    return redirect("booking_list")
# core/models.py (inside Booking)
def can_cancel(self):
    from django.utils import timezone
    return (
        self.status == Booking.Status.CONFIRMED
        and self.travel_option.departure_at > timezone.now()
    )

