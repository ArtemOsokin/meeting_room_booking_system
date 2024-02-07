import datetime
import typing

import pytest
from faker import Faker
from pytest import fixture
from rest_framework.test import APIClient

from mrbs_app.models import Reservation, Room


@fixture()
def random_password(faker: Faker) -> str:
    return faker.password()


@fixture()
def random_username(faker: Faker) -> str:
    return faker.user_name()


@fixture()
def password(faker: Faker) -> str:
    return faker.password()


@fixture()
@pytest.mark.django_db
def user(django_user_model, faker: Faker, password):
    return django_user_model.objects.create_user(
        username=faker.user_name(),
        password=password,
        email=faker.email(),
        first_name=faker.first_name(),
        last_name=faker.last_name(),
    )


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def room_creator(faker) -> typing.Callable[[], Room]:
    def _create() -> Room:
        room = Room(
            number=faker.unique.random_int(min=1, max=30),
            name=faker.unique.bothify(text='Room_#'),
        )
        room.save()
        return room

    return _create


@pytest.fixture
def reservation_creator(user, room_creator, faker) -> typing.Callable[[], Reservation]:
    def _create() -> Reservation:
        reservation = Reservation(
            reserved_from=datetime.datetime.utcnow(),
            reserved_to=datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            purpose_of_booking=faker.unique.bothify(text='purpose_???'),
            user=user,
            room=room_creator(),
            status=Reservation.ReservationStatus.ACTIVE,
        )
        reservation.save()
        return reservation

    return _create
