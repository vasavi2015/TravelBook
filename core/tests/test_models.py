import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import TravelOption, Booking

@pytest.mark.django_db
def test_create_and_cancel_booking():
    user = User.objects.create_user('alice', password='pass12345')
    opt = TravelOption.objects.create(
        travel_id='TR001', type='BUS', source='A', destination='B',
        departure_at=timezone.now() + timezone.timedelta(days=1),
        price=100, available_seats=10
    )
    booking = Booking.create_booking(user=user, travel_option_id=opt.id, seats=3)
    opt.refresh_from_db()
    assert booking.total_price == 300
    assert opt.available_seats == 7

    booking.cancel()
    opt.refresh_from_db()
    assert booking.status == 'CANCELLED'
    assert opt.available_seats == 10

@pytest.mark.django_db
def test_not_enough_seats():
    user = User.objects.create_user('bob', password='pass12345')
    opt = TravelOption.objects.create(
        travel_id='TR002', type='TRAIN', source='X', destination='Y',
        departure_at=timezone.now() + timezone.timedelta(days=1),
        price=200, available_seats=1
    )
    with pytest.raises(ValidationError):
        Booking.create_booking(user=user, travel_option_id=opt.id, seats=2)
