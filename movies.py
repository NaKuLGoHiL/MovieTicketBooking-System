"""
Movie Ticket Booking System - Data Layer
Contains movie data, showtimes, and seat management
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Movie:
    id: int
    title: str
    genre: str
    duration_min: int
    rating: str
    description: str
    language: str = "English"

    def __str__(self):
        return f"[{self.id}] {self.title} ({self.rating}) | {self.genre} | {self.duration_min} min | {self.language}"


@dataclass
class Showtime:
    id: int
    movie_id: int
    hall: str
    date_time: datetime
    total_seats: int
    booked_seats: list = field(default_factory=list)
    price: float = 250.0

    @property
    def available_seats(self):
        return self.total_seats - len(self.booked_seats)

    def is_seat_available(self, seat: str) -> bool:
        return seat not in self.booked_seats

    def book_seat(self, seat: str) -> bool:
        if self.is_seat_available(seat):
            self.booked_seats.append(seat)
            return True
        return False

    def get_seat_map(self) -> dict:
        """Returns a dict of all seats with their availability status."""
        rows = "ABCDE"
        cols = range(1, 11)
        seat_map = {}
        for row in rows:
            for col in cols:
                seat = f"{row}{col}"
                seat_map[seat] = seat not in self.booked_seats
        return seat_map


@dataclass
class Booking:
    booking_id: str
    user_name: str
    showtime_id: int
    movie_title: str
    seats: list
    total_price: float
    booked_at: datetime = field(default_factory=datetime.now)
    hall: str = ""
    show_datetime: datetime = None

    def receipt(self) -> str:
        seats_str = ", ".join(self.seats)
        show_time_str = self.show_datetime.strftime("%d %b %Y, %I:%M %p") if self.show_datetime else "N/A"
        return (
            f"\n{'='*50}\n"
            f"  🎬  BOOKING CONFIRMATION\n"
            f"{'='*50}\n"
            f"  Booking ID   : {self.booking_id}\n"
            f"  Name         : {self.user_name}\n"
            f"  Movie        : {self.movie_title}\n"
            f"  Hall         : {self.hall}\n"
            f"  Show Time    : {show_time_str}\n"
            f"  Seats        : {seats_str}\n"
            f"  Total Paid   : ₹{self.total_price:.2f}\n"
            f"  Booked At    : {self.booked_at.strftime('%d %b %Y, %I:%M %p')}\n"
            f"{'='*50}\n"
            f"  Enjoy your movie! 🍿\n"
            f"{'='*50}\n"
        )


# ─────────────────────────────────────────────
#  Seed Data
# ─────────────────────────────────────────────

MOVIES = [
    Movie(1, "Interstellar",    "Sci-Fi",   169, "PG-13", "A team of explorers travel through a wormhole in space.",  "English"),
    Movie(2, "Pathaan",         "Action",   146, "UA",    "A spy returns from exile to stop a massive terror plot.",   "Hindi"),
    Movie(3, "RRR",             "Action",   182, "UA",    "Two legendary rebels fight against British colonial rule.", "Telugu"),
    Movie(4, "The Dark Knight", "Action",   152, "PG-13", "Batman faces the Joker in a battle for Gotham's soul.",    "English"),
    Movie(5, "Inception",       "Thriller", 148, "PG-13", "A thief who enters dreams to steal secrets.",              "English"),
]

from datetime import timedelta

_base = datetime(2026, 3, 29, 10, 0)

SHOWTIMES = [
    Showtime(1,  1, "Hall A", _base,                      50, price=350.0),
    Showtime(2,  1, "Hall B", _base + timedelta(hours=3), 50, price=300.0),
    Showtime(3,  2, "Hall A", _base + timedelta(hours=6), 50, price=250.0),
    Showtime(4,  2, "Hall C", _base + timedelta(days=1),  50, price=200.0),
    Showtime(5,  3, "Hall B", _base + timedelta(hours=2), 50, price=400.0),
    Showtime(6,  4, "Hall A", _base + timedelta(hours=5), 50, price=300.0),
    Showtime(7,  5, "Hall C", _base + timedelta(hours=4), 50, price=350.0),
]
