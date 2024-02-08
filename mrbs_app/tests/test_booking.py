import datetime as dt
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
        'reserved_from': dt.datetime.utcnow(),
        'reserved_to': dt.datetime.utcnow() + dt.timedelta(hours=1),
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
        'reserved_from': dt.datetime.utcnow(),
        'reserved_to': dt.datetime.utcnow() - dt.timedelta(hours=1),
    }
    api_client.force_authenticate(user=user)
    response = api_client.post(reverse('reservation'), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert tuple(json.loads(response.content)) == HTTPErrorMessages.INCORRECT_RESERVATION_TIME


def test_get_reservations(faker, room_creator, user, api_client):
    room = room_creator()
    len_reservations = 2
    reserved_time = dt.datetime.utcnow()
    fake_reservations = [
        Reservation(
            reserved_from=reserved_time + dt.timedelta(hours=i),
            reserved_to=reserved_time + dt.timedelta(hours=i + 0.9),
            purpose_of_booking=faker.unique.bothify(text='purpose_???'),
            user=user,
            room=room,
            status=Reservation.ReservationStatus.ACTIVE,
        )
        for i in range(len_reservations)
    ]
    Reservation.objects.bulk_create(fake_reservations)
    url = (
        f'{reverse("reservations")}?'
        f'reserved_from={reserved_time}&'
        f'reserved_to={reserved_time+dt.timedelta(hours=len_reservations)}&'
        f'room_id={room.id}'
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    response_data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == len_reservations
    for i in range(len_reservations):
        assert response_data[i]['id'] == fake_reservations[i].id
        assert response_data[i]['purpose_of_booking'] == fake_reservations[i].purpose_of_booking
        assert (
            response_data[i]['reserved_from']
            == fake_reservations[i].reserved_from.isoformat() + 'Z'
        )
        assert response_data[i]['reserved_to'] == fake_reservations[i].reserved_to.isoformat() + 'Z'
        assert response_data[i]['status'] == fake_reservations[i].status


def test_get_reservations_empty(faker, user, api_client):
    reserved_time = dt.datetime.utcnow()
    url = (
        f'{reverse("reservations")}?'
        f'reserved_from={reserved_time}&'
        f'reserved_to={reserved_time+dt.timedelta(hours=1)}&'
        f'room_id=1'
    )
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    response_data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == 0
    assert response_data == []
