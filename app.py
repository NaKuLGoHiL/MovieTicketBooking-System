from flask import Flask, request, render_template, jsonify
from booking_engine import BookingEngine

app = Flask(__name__)
engine = BookingEngine()

@app.route('/')
def home():
    return render_template('cineplex.html')

@app.route('/book', methods=['POST'])
def book():
    try:
        data = request.get_json()

        user_name = data['name']
        showtime_id = int(data['showtime'])
        seats = data['seats']

        success, result = engine.book_tickets(user_name, showtime_id, seats)

        if success:
            return jsonify({"success": True, "message": f"Booking Successful! ID: {result}"})
        else:
            return jsonify({"success": False, "message": result})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"success": False, "message": "Server error"})
    
@app.route('/get-bookings')
def get_bookings():
    from db import connect_db

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM bookings")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"bookings": data}

if __name__ == '__main__':
    app.run(debug=True, port=5001)

    