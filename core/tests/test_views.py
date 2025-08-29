import pytest
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from core.models import TravelOption

@pytest.mark.django_db
def test_travel_list_view(client):
    TravelOption.objects.create(
        travel_id='TR003', type='FLIGHT', source='Hyd', destination='Vizag',
        departure_at=timezone.now() + timezone.timedelta(days=3),
        price=5000, available_seats=20
    )
    resp = client.get(reverse('travel_list'))
    assert resp.status_code == 200
    assert b'Available Travel Options' in resp.content
