import datetime
import json

from django.urls import reverse
from rest_framework import status

from mrbs_app.api.error_messages import HTTPErrorMessages
from mrbs_app.models import Reservation


def test_create_reservation(faker, room_creator, user, api_client):
    room = room_creator()
    data = {
        'room_id': room.id,
        'purpose_of_booking': faker.bothify('Purpose_???'),
        'reserved_from': datetime.datetime.utcnow(),
        'reserved_to': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    api_client.force_authenticate(user=user)
    response = api_client.post(reverse('reservation'), data=data)
    assert response.status_code == status.HTTP_201_CREATED

    reservation = Reservation.objects.all().first()
    assert reservation.reserved_to.strftime('%m/%d/%Y') == data['reserved_to'].strftime('%m/%d/%Y')
    assert reservation.reserved_from.strftime('%m/%d/%Y') == data['reserved_from'].strftime(
        '%m/%d/%Y'
    )
    assert reservation.purpose_of_booking == data['purpose_of_booking']
    assert reservation.id == 1


def test_create_reservation_is_busy(faker, reservation_creator, user, api_client):
    reservation = reservation_creator()
    data = {
        'room_id': reservation.room.id,
        'purpose_of_booking': reservation.purpose_of_booking,
        'reserved_from': reservation.reserved_from,
        'reserved_to': reservation.reserved_to,
    }
    api_client.force_authenticate(user=user)
    response = api_client.post(reverse('reservation'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert tuple(json.loads(response.content)[0]) == HTTPErrorMessages.BOOKING_TIME_IS_BUSY[0]


def test_create_reservation_incorrect(faker, room_creator, user, api_client):
    room = room_creator()
    data = {
        'room_id': room.id,
        'purpose_of_booking': faker.bothify('Purpose_???'),
        'reserved_from': datetime.datetime.utcnow(),
        'reserved_to': datetime.datetime.utcnow() - datetime.timedelta(hours=1),
    }
    api_client.force_authenticate(user=user)
    response = api_client.post(reverse('reservation'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert tuple(json.loads(response.content)) == HTTPErrorMessages.INCORRECT_RESERVATION_TIME
