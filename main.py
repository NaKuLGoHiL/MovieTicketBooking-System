"""
🎬 Movie Ticket Booking System - CLI
Run this file to start the interactive booking experience.
"""

from booking_engine import BookingEngine

engine = BookingEngine()

# ─────────────────────────────────────────────
#  Display helpers
# ─────────────────────────────────────────────

def banner():
    print("""
╔══════════════════════════════════════════════════════╗
║        🎬  CINEPLEX TICKET BOOKING SYSTEM  🎬        ║
╚══════════════════════════════════════════════════════╝""")


def menu():
    print("""
┌──────────────────────────────┐
│  MAIN MENU                   │
│  1. Browse Movies            │
│  2. View Showtimes           │
│  3. Book Tickets             │
│  4. View Seat Map            │
│  5. My Booking               │
│  6. Cancel Booking           │
│  7. Exit                     │
└──────────────────────────────┘""")


def display_movies():
    print("\n" + "─" * 55)
    print("  🎞  NOW SHOWING")
    print("─" * 55)
    for movie in engine.movies.values():
        print(f"  {movie}")
        print(f"     {movie.description}")
        print()


def display_showtimes(movie_id: int):
    movie = engine.get_movie(movie_id)
    if not movie:
        print("  ❌  Movie not found.")
        return

    showtimes = engine.get_showtimes_for_movie(movie_id)
    if not showtimes:
        print("  ❌  No showtimes available.")
        return

    print(f"\n  🎬  Showtimes for: {movie.title}")
    print("  " + "─" * 55)
    print(f"  {'ID':<5} {'Hall':<8} {'Date & Time':<22} {'Available':<12} {'Price'}")
    print("  " + "─" * 55)
    for s in showtimes:
        dt_str = s.date_time.strftime("%d %b %Y  %I:%M %p")
        print(f"  {s.id:<5} {s.hall:<8} {dt_str:<22} {s.available_seats}/{s.total_seats}{'':5} ₹{s.price:.0f}")


def display_seat_map(showtime_id: int):
    showtime = engine.get_showtime(showtime_id)
    if not showtime:
        print("  ❌  Showtime not found.")
        return

    seat_map = showtime.get_seat_map()
    print(f"\n  🪑  Seat Map — {showtime.hall} | Showtime #{showtime.id}")
    print()
    print("      " + "  ".join(str(i) for i in range(1, 11)))
    print("      " + "─" * 29)
    for row in "ABCDE":
        row_display = []
        for col in range(1, 11):
            seat = f"{row}{col}"
            row_display.append("✅" if seat_map[seat] else "❌")
        print(f"  {row} |  " + "  ".join(row_display))
    print()
    print("  ✅ = Available   ❌ = Booked")


# ─────────────────────────────────────────────
#  Flow handlers
# ─────────────────────────────────────────────

def flow_browse():
    display_movies()


def flow_showtimes():
    display_movies()
    try:
        mid = int(input("\n  Enter Movie ID: ").strip())
    except ValueError:
        print("  ❌  Invalid input.")
        return
    display_showtimes(mid)


def flow_book():
    display_movies()
    try:
        mid = int(input("\n  Enter Movie ID: ").strip())
    except ValueError:
        print("  ❌  Invalid movie ID.")
        return

    display_showtimes(mid)
    showtimes = engine.get_showtimes_for_movie(mid)
    if not showtimes:
        return

    try:
        sid = int(input("\n  Enter Showtime ID: ").strip())
    except ValueError:
        print("  ❌  Invalid showtime ID.")
        return

    showtime = engine.get_showtime(sid)
    if not showtime or showtime.movie_id != mid:
        print("  ❌  Showtime not found for this movie.")
        return

    display_seat_map(sid)

    name = input("  Enter your name: ").strip()
    if not name:
        print("  ❌  Name cannot be empty.")
        return

    seats_input = input("  Enter seats (e.g. A1,B2,C3): ").strip().upper()
    seats = [s.strip() for s in seats_input.split(",") if s.strip()]
    if not seats:
        print("  ❌  No seats entered.")
        return

    price_preview = showtime.price * len(seats)
    print(f"\n  Total: ₹{price_preview:.2f} for {len(seats)} seat(s)")
    confirm = input("  Confirm booking? (y/n): ").strip().lower()
    if confirm != "y":
        print("  ⚠️   Booking cancelled.")
        return

    success, result = engine.book_tickets(name, sid, seats)
    if success:
        booking = engine.get_booking(result)
        print(booking.receipt())
    else:
        print(f"  ❌  {result}")


def flow_seat_map():
    try:
        sid = int(input("\n  Enter Showtime ID: ").strip())
    except ValueError:
        print("  ❌  Invalid input.")
        return
    display_seat_map(sid)


def flow_view_booking():
    bid = input("\n  Enter Booking ID: ").strip().upper()
    booking = engine.get_booking(bid)
    if booking:
        print(booking.receipt())
    else:
        print("  ❌  Booking not found.")


def flow_cancel():
    bid = input("\n  Enter Booking ID to cancel: ").strip().upper()
    confirm = input(f"  Cancel booking {bid}? (y/n): ").strip().lower()
    if confirm != "y":
        print("  ⚠️   Cancellation aborted.")
        return
    success, msg = engine.cancel_booking(bid)
    print(f"  {'✅' if success else '❌'}  {msg}")


# ─────────────────────────────────────────────
#  Main loop
# ─────────────────────────────────────────────

def main():
    banner()
    handlers = {
        "1": flow_browse,
        "2": flow_showtimes,
        "3": flow_book,
        "4": flow_seat_map,
        "5": flow_view_booking,
        "6": flow_cancel,
    }
    while True:
        menu()
        choice = input("  Select option: ").strip()
        if choice == "7":
            print("\n  👋  Thanks for using CinePlex! Goodbye.\n")
            break
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("  ❌  Invalid option. Please try again.")


if __name__ == "__main__":
    main()
