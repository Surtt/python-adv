from dataclasses import dataclass, field


@dataclass
class Room:
    number: int
    price: float

    def get_price(self):
        return self.price


@dataclass
class LuxuryRoom(Room):
    multiplier: float = 1.0

    def get_price(self):
        return self.price * self.multiplier


@dataclass
class Booking:
    room: Room
    guest_name: str
    check_in: str
    check_out: str
    is_cancelled: bool = False

    def cancel(self):
        self.is_cancelled = True


@dataclass
class Hotel:
    rooms: list[Room] = field(default_factory=list)
    bookings: list[Booking] = field(default_factory=list)

    def add_room(self, room):
        self.rooms.append(room)

    def book(self, room, guest_name, check_in, check_out):
        self.bookings.append(Booking(room, guest_name, check_in, check_out))

    def cancel_booking(self, booking):
        booking.cancel()

    def available_rooms(self, check_in, check_out):
        return [
            room
            for room in self.rooms
            if not any(
                booking.room == room
                and not booking.is_cancelled
                and booking.check_in < check_out
                and check_in < booking.check_out
                for booking in self.bookings
            )
        ]

    def show_bookings(self):
        return self.bookings


room = Room(1, 100)
lux_room = LuxuryRoom(2, 200, 2)
booking = Booking(room, "Alex", "2026-05-05", "2026-05-10")
hotel = Hotel(rooms=[room, lux_room], bookings=[booking])

print(hotel.available_rooms("2026-05-05", "2026-05-10"))
print(hotel.available_rooms("2026-06-01", "2026-06-05"))
print(room.get_price())
print(lux_room.get_price())
hotel.cancel_booking(booking)
print(hotel.available_rooms("2026-05-05", "2026-05-10"))
