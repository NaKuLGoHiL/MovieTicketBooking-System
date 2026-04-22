import uuid
from movies import MOVIES, SHOWTIMES, Booking
from db import connect_db

class BookingEngine:
    def __init__(self):
        self.movies = {m.id: m for m in MOVIES}
        self.showtimes = {s.id: s for s in SHOWTIMES}
        self.bookings = {}

    def get_movie(self, movie_id):
        return self.movies.get(movie_id)

    def get_showtime(self, showtime_id):
        return self.showtimes.get(showtime_id)

    def book_tickets(self, user_name, showtime_id, seats):
        showtime = self.get_showtime(showtime_id)
        if not showtime:
            return False, "Showtime not found"

        movie = self.get_movie(showtime.movie_id)

        for seat in seats:
            if seat in showtime.booked_seats:
                return False, f"Seat {seat} already booked"

        for seat in seats:
            showtime.booked_seats.append(seat)

        booking_id = "BK" + uuid.uuid4().hex[:6].upper()

        # ✅ SAVE TO DATABASE
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO bookings 
                (booking_id, user_name, movie_title, showtime_id, seats, total_price)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                booking_id,
                user_name,
                movie.title,
                showtime_id,
                ",".join(seats),
                showtime.price * len(seats)
            ))

            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            print("DB ERROR:", e)
            return False, "Database error"

        return True, booking_id