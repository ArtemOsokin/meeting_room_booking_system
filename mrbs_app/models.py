from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedIDMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Room(TimeStampedIDMixin):
    number = models.IntegerField(blank=False, null=False)
    name = models.CharField(max_length=32, blank=False, null=False)


class Reservation(TimeStampedIDMixin):
    class ReservationStatus(models.TextChoices):
        ACTIVE = 'active', _('Active')
        CANCELLED = 'cancelled', _('Cancelled')
        COMPLETED = 'completed', _('Completed')

    purpose_of_booking = models.CharField(max_length=256)
    reserved_from = models.DateTimeField()
    reserved_to = models.DateTimeField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=ReservationStatus.choices)
