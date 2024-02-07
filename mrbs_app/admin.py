from django.contrib import admin

from mrbs_app.models import Reservation, Room


@admin.register(Room, Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass
