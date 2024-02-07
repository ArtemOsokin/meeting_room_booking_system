class BookingErrorBase(Exception):
    pass


class ReservationBusyError(BookingErrorBase):
    pass


class ReservationTimeError(BookingErrorBase):
    pass
